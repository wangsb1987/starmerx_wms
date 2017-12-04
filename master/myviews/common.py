# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from master.models import T_user
from master.models import ResUsers
from master.models import ResPartner,ResProduct
from master.models import AccountInvoice, AccountInvoiceLine
from master.models import PaymentMode
from master.models import ResCurrency
from django import forms
from django.http import HttpResponseRedirect
import json
from django.db import connection, transaction

import json
import pytz
import types
from django.db import models
from decimal import *
from django.db.models.base import ModelState
from datetime import datetime,date
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.db.models import Q

# ---登录控件
class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'value': ''}))
    userpsw = forms.CharField(widget=forms.TextInput(attrs={'value': '', 'type': 'password'}))

# ---登录
def login(req):
    print req.POST.get('uname', 1)
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            m = ResUsers.objects.get(login=req.POST['username'])
            if m.password == req.POST['userpsw']:
                req.session['login_t_id'] = m.id
                partner = ResPartner.objects.get(id=m.partner_id)
                req.session['login_t_name'] = partner.name
                print "You're logged in."
                print req.session.get('login_t_id', default=None)

                return HttpResponseRedirect('/mainform')
            else:
                print "Your username and password didn't match."
                return HttpResponse('登陆失败')
    else:
        form = UserForm()

    return render_to_response('login.html', {'form': form})

# ---退出登录
def logout(req):
    form = UserForm(req.POST)
    try:
        del req.session['login_t_id']
        del req.session['login_t_name']
    except KeyError:
        pass
    # return HttpResponseRedirect('/login')
    # 通过js来跳转页面，取巧
    jump_to_console = '''<html><body onLoad="window.top.location.href='/login'" ></body></html>'''
    response = HttpResponse(jump_to_console)
    # response.set_cookie("username", username)
    return response

# ---主页
def mainform(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    return render_to_response('mainform.html', {'login_t_name': username})

# ---欢迎页面
def main(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    return render_to_response('main.html', {'login_t_name': username})

# ---个人设置
def profile(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    return render_to_response('profile.html', {'login_t_name': username})

#获取产品下拉列表
def getProducts(request):
    '''select2 分页获取product, 因为product实在是太多啦,页面直接卡死'''
    name = request.GET.get("name", None)
    page = request.GET.get("page", 1)
    page = int(page) - 1
    skip = page * 10
    data = {}
    if name:
        products, count = get_skip_by_name_product(name, skip)
        data['products'] = products
        data['count'] = count
    else:
        products, count = get_first_10_products(skip)
        data['products'] = products
        data['count'] = count
    more = page * 10 < data['count']
    data['more'] = more
    print data
    post_result = {
        'ret': 0,
        'message': '',
        'data': data
    }
    return HttpResponse(json_encode(post_result), content_type="application/json")

def get_skip_by_name_product(name, skip):

    temp = ResProduct.objects.filter(Q(name_template__icontains=name)|Q(default_code__icontains=name)).filter(product_tmpl__type='product',product_tmpl__purchase_ok='t').values('id', 'name_template','default_code','last_purchase_price')
    count = temp.count()
    if count < skip+10:
        data = temp[skip:]
    else:
        data = temp[skip:skip+10]
    return data, count


def get_first_10_products(skip):
    count = ResProduct.objects.filter(product_tmpl__type='product',product_tmpl__purchase_ok='t').count()
    data = ResProduct.objects.filter(product_tmpl__type='product',product_tmpl__purchase_ok='t').values('id', 'name_template','default_code','last_purchase_price')[skip:skip+10]
    return data, count


#获取供应商下拉列表
def getSupplier(request):
    '''select2 分页获取Supplier, 因为Supplier实在是太多啦,页面直接卡死'''
    name = request.GET.get("name", None)
    page = request.GET.get("page", 1)
    page = int(page) - 1
    skip = page * 10
    data = {}
    if name:
        supplier, count = get_skip_by_name_supplier(name, skip)
        data['supplier'] = supplier
        data['count'] = count
    else:
        supplier, count = get_first_10_supplier(skip)
        data['supplier'] = supplier
        data['count'] = count
    more = page * 10 < data['count']
    data['more'] = more
    print data
    post_result = {
        'ret': 0,
        'message': '',
        'data': data
    }
    return HttpResponse(json_encode(post_result), content_type="application/json")

def get_skip_by_name_supplier(name, skip):

    temp = ResPartner.objects.filter(name__icontains=name).filter(active='t').values('id', 'name')
    count = temp.count()
    if count < skip+10:
        data = temp[skip:]
    else:
        data = temp[skip:skip+10]
    return data, count


def get_first_10_supplier(skip):
    count = ResPartner.objects.all().count()
    data = ResPartner.objects.all().values('id', 'name')[skip:skip+10]
    return data, count


def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has 
    problems with some models).
    """

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        elif isinstance(data, ModelState):
            ret = None
        elif isinstance(data, datetime):
            ret = data.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.CN_TIME_ZONE)).strftime(
                '%Y-%m-%d %H:%M:%S')
        elif isinstance(data, date):
            ret = data.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.CN_TIME_ZONE)).strftime('%Y-%m-%d')
            # elif isinstance(data, django.db.models.fields.related.RelatedManager):
            #    ret = _list(data.all())
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)
    return json.dumps(ret)