# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from master.models import T_user
from master.models import ResUsers
from master.models import ResPartner
from master.models import AccountInvoice, AccountInvoiceLine
from master.models import PaymentMode
from master.models import ResCurrency
from django import forms
from django.http import HttpResponseRedirect
import json
from django.db import connection, transaction


# Create your views here.
class Person(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def say(self):
        return "I'm " + self.name

# ---登录控件
class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'value': 'admin'}))
    userpsw = forms.CharField(widget=forms.TextInput(attrs={'value': 'Smerx1216', 'type': 'password'}))

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
    return HttpResponseRedirect('/login')

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

# ---财务管理/发票列表页面
def cwgl_invoice_list(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    if not username:
        return logout(req)
    return render_to_response('starmerx_cwgl/invoice_list.html', {'login_t_name': username})

# ---财务管理/发票审核页面
def cwgl_invoice_sh(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    return render_to_response('starmerx_cwgl/invoice_sh.html', {'login_t_name': username})

# ---财务管理/发票明细页面
def cwgl_invoice_info(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    invoice_obj = AccountInvoice.objects.get(id = req.GET['invoice_id'])
    dict1 = {}

    def state_help(argument):
        switcher = {
            'draft': "草稿",
            'validate': "待支付",
            'open': "待审核",
            'partPaid': "部分支付",
            'paid': "已付",
            'closed': "已结案",
            'cancel': "已取消",
        }
        return switcher.get(argument, "nothing")
    if invoice_obj:
        dict1['id'] = invoice_obj.id
        # 供应商
        if invoice_obj.partner_id:
            partner = ResPartner.objects.get(id=invoice_obj.partner_id)
            dict1['partner'] = partner.name
        else:
            dict1['partner'] = ''
        if invoice_obj.date_invoice:
            dict1['date_invoice'] = invoice_obj.date_invoice.strftime('%Y-%m-%d')
        else:
            dict1['date_invoice'] = ''
        dict1['number'] = invoice_obj.number
        # 销售员
        if invoice_obj.user_id:
            user = ResUsers.objects.get(id=invoice_obj.user_id)
            userp = ResPartner.objects.get(id=user.partner_id)
            dict1['user'] = userp.name
        else:
            dict1['user'] = ''
        # 付款方式
        if invoice_obj.payment_mode:
            payment = PaymentMode.objects.get(id=invoice_obj.payment_mode)
            dict1['payment_mode'] = payment.name
        else:
            dict1['payment_mode'] = ''
        if invoice_obj.date_due:
            dict1['date_due'] = invoice_obj.date_due.strftime('%Y-%m-%d')
        else:
            dict1['date_due'] = ''
        dict1['origin'] = invoice_obj.origin
        # 币种
        biz = ResCurrency.objects.get(id=invoice_obj.currency_id)
        dict1['currency'] = biz.name
        dict1['currency_symbol'] = biz.symbol
        dict1['residual'] = float(invoice_obj.residual)
        # 小计
        dict1['amount_untaxed'] = float(invoice_obj.amount_untaxed)
        # 合计
        dict1['amount_total'] = float(invoice_obj.amount_total)

        dict1['state'] = state_help(invoice_obj.state)
        line_objs = AccountInvoiceLine.objects.filter(invoice_id=invoice_obj.id)
        line_list = []
        for lineitem in line_objs:
            line_dict = {}
            line_dict['name'] = lineitem.name
            line_dict['quantity'] = int(lineitem.quantity)
            line_dict['price_unit'] = float(lineitem.price_unit)
            lastacline = AccountInvoiceLine.objects.filter(product_id=lineitem.product_id).exclude(
                invoice__state__in=['draft', 'cancel']).order_by(
                '-create_date').first()
            if lastacline:
                line_dict['price_last'] = float(lastacline.price_unit)
            else:
                line_dict['price_last'] = "无数据"
            line_list.append(line_dict)
        dict1['product_list'] = line_list
        dict1['comment'] = invoice_obj.comment
        dict1['amount_tax'] = invoice_obj.amount_tax
        dict1['discount_amount'] = invoice_obj.discount_amount

    return render_to_response('starmerx_cwgl/invoice_info.html', {'invoice_obj': dict1})

# ---测试使用
def bootstrap_table_test(req):
    username = req.session.get('login_t_name', default=None)
    return render_to_response('bootstrap_table_test.html', {'login_t_name': username})


# ---测试使用
def return_bootstrap_data(req):
    stra = {'total': 100,
            'rows': [{'id': 1, 'name': 'zhangsan', 'price': '12.5'}, {'id': 2, 'name': 'lisi', 'price': '12.5'}]}
    return HttpResponse(json.dumps(stra), content_type="application/json")

# ---财务管理/发票列表获取数据
def get_invoice_list(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    order = 'asc'
    limit = 20
    offset = 0
    if req.GET.has_key('order'):
        order = req.GET['order']
    if req.GET.has_key('limit'):
        limit = int(req.GET['limit'])
    if req.GET.has_key('offset'):
        offset = int(req.GET['offset'])
    startjilu = int(offset)
    endjilu = int(offset) + int(limit)
    filterdist = {}
    if req.GET.has_key('paymode') and req.GET['paymode'] != "0":
        filterdist['payment_mode'] = req.GET['paymode']
    if req.GET.has_key('state') and req.GET['state'] != "0":
        filterdist['state'] = req.GET['state']
    if req.GET.has_key('origin') and req.GET['origin'] != "":
        filterdist['origin'] = req.GET['origin']

    # account_objs = AccountInvoice.objects.raw('SELECT * FROM account_invoice where ' + searchstr)[startjilu:endjilu]
    account_objs = AccountInvoice.objects.filter(**filterdist)

    # cursor = connection.cursor()
    # cursor.execute("SELECT count(0) FROM account_invoice where " + searchstr)
    # zongrowcount = cursor.fetchone()
    zongrowcount = account_objs.count()

    zongdict = {}
    list1 = []

    def state_help(argument):
        switcher = {
            'draft': "草稿",
            'validate': "待支付",
            'open': "待审核",
            'partPaid': "部分支付",
            'paid': "已付",
            'closed': "已结案",
            'cancel': "已取消",
        }
        return switcher.get(argument, "nothing")

    for acitem in account_objs[startjilu:endjilu]:
        dict1 = {}
        dict1['id'] = acitem.id
        # 供应商
        if acitem.partner_id:
            partner = ResPartner.objects.get(id=acitem.partner_id)
            dict1['partner'] = partner.name
        else:
            dict1['partner'] = ''
        if acitem.date_invoice:
            dict1['date_invoice'] = acitem.date_invoice.strftime('%Y-%m-%d')
        else:
            dict1['date_invoice'] = ''
        dict1['number'] = acitem.number
        # 销售员
        if acitem.user_id:
            user = ResUsers.objects.get(id=acitem.user_id)
            userp = ResPartner.objects.get(id=user.partner_id)
            dict1['user'] = userp.name
        else:
            dict1['user'] = ''
        # 付款方式
        if acitem.payment_mode:
            payment = PaymentMode.objects.get(id=acitem.payment_mode)
            dict1['payment_mode'] = payment.name
        else:
            dict1['payment_mode'] = ''
        if acitem.date_due:
            dict1['date_due'] = acitem.date_due.strftime('%Y-%m-%d')
        else:
            dict1['date_due'] = ''
        dict1['origin'] = acitem.origin
        # 币种
        biz = ResCurrency.objects.get(id=acitem.currency_id)
        dict1['currency'] = biz.name
        dict1['residual'] = float(acitem.residual)
        # 小计
        dict1['amount_untaxed'] = float(acitem.amount_untaxed)
        # 合计
        dict1['amount_total'] = float(acitem.amount_total)

        dict1['state'] = state_help(acitem.state)
        line_objs = AccountInvoiceLine.objects.filter(invoice_id=acitem.id)
        line_list = []
        for lineitem in line_objs:
            line_dict = {}
            line_dict['name'] = lineitem.name
            line_dict['quantity'] = int(lineitem.quantity)
            line_dict['price_unit'] = float(lineitem.price_unit)
            lastacline = AccountInvoiceLine.objects.filter(product_id=lineitem.product_id).exclude(
                invoice__state__in=['draft', 'cancel']).order_by(
                '-create_date').first()
            if lastacline:
                line_dict['price_last'] = float(lastacline.price_unit)
            else:
                line_dict['price_last'] = "无数据"
            line_list.append(line_dict)
        dict1['product_list'] = line_list
        list1.append(dict1)
    zongdict['total'] = zongrowcount

    zongdict['rows'] = list1
    return HttpResponse(json.dumps(zongdict), content_type="application/json")

# ---财务管理/发票审核获取数据
def get_invoice_sh(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    order = 'asc'
    limit = 20
    offset = 0
    if req.GET.has_key('order'):
        order = req.GET['order']
    if req.GET.has_key('limit'):
        limit = int(req.GET['limit'])
    if req.GET.has_key('offset'):
        offset = int(req.GET['offset'])
    startjilu = int(offset)
    endjilu = int(offset) + int(limit)
    searchstr = "state='draft'"
    scpsign = False
    scpxsign = False
    if req.GET.has_key('paymode') and req.GET['paymode'] != "0":
        searchstr += " and payment_mode=" + req.GET['paymode']
    if req.GET.has_key('scp') and req.GET['scp'] != "0":
        scpsign = True  # 筛选>上次采购价的百分比
        # searchstr += " and payment_mode=" + req.GET['paymode']
    if req.GET.has_key('scpx') and req.GET['scpx'] != "0":
        scpxsign = True  # 筛选《=上次采购价
        # searchstr += " and payment_mode=" + req.GET['paymode']
    if req.GET.has_key('amount_total') and req.GET['amount_total'] != "":
        searchstr += " and amount_total<=" + req.GET['amount_total']
    if req.GET.has_key('origin') and req.GET['origin'] != "":
        searchstr += " and origin='" + req.GET['origin'] + "'"

    # =================第一次筛选
    account_objs = AccountInvoice.objects.raw('SELECT * FROM account_invoice where ' + searchstr)[startjilu:endjilu]
    # account_objs = AccountInvoice.objects.filter(searchstr)[startjilu:endjilu]
    aaa = account_objs
    cursor = connection.cursor()
    cursor.execute("SELECT count(0) FROM account_invoice where " + searchstr)
    zongrowcount = cursor.fetchone()

    # =================第一次筛选end


    zongdict = {}
    list1 = []

    for acitem in account_objs:
        dict1 = {}
        dict1['id'] = acitem.id
        # 供应商
        if acitem.partner_id:
            partner = ResPartner.objects.get(id=acitem.partner_id)
            dict1['partner'] = partner.name
        else:
            dict1['partner'] = ''
        if acitem.date_invoice:
            dict1['date_invoice'] = acitem.date_invoice.strftime('%Y-%m-%d')
        else:
            dict1['date_invoice'] = ''
        dict1['number'] = acitem.number
        # 销售员
        if acitem.user_id:
            user = ResUsers.objects.get(id=acitem.user_id)
            userp = ResPartner.objects.get(id=user.partner_id)
            dict1['user'] = userp.name
        else:
            dict1['user'] = ''
        # 付款方式
        if acitem.payment_mode:
            payment = PaymentMode.objects.get(id=acitem.payment_mode)
            dict1['payment_mode'] = payment.name
        else:
            dict1['payment_mode'] = ''
        if acitem.date_due:
            dict1['date_due'] = acitem.date_due.strftime('%Y-%m-%d')
        else:
            dict1['date_due'] = ''
        dict1['origin'] = acitem.origin
        # 币种
        biz = ResCurrency.objects.get(id=acitem.currency_id)
        dict1['currency'] = biz.name
        dict1['residual'] = float(acitem.residual)
        # 小计
        dict1['amount_untaxed'] = float(acitem.amount_untaxed)
        # 合计
        dict1['amount_total'] = float(acitem.amount_total)

        dict1['state'] = '草稿'
        line_objs = AccountInvoiceLine.objects.filter(invoice_id=acitem.id)
        line_list = []
        for lineitem in line_objs:
            line_dict = {}
            line_dict['name'] = lineitem.name
            line_dict['quantity'] = int(lineitem.quantity)
            line_dict['price_unit'] = float(lineitem.price_unit)
            lastacline = AccountInvoiceLine.objects.filter(product_id=lineitem.product_id).exclude(
                invoice__state__in=['draft', 'cancel']).order_by(
                '-create_date').first()
            if lastacline:
                line_dict['price_last'] = float(lastacline.price_unit)
            else:
                line_dict['price_last'] = "无数据"
            line_list.append(line_dict)
        dict1['product_list'] = line_list

        list1.append(dict1)

    zongdict['total'] = zongrowcount
    # zongdict['zongpages'] = zongpages
    # zongdict['pageindex'] = pageindex
    zongdict['rows'] = list1
    return HttpResponse(json.dumps(zongdict), content_type="application/json")


# ---个人设置
def profile(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    return render_to_response('profile.html', {'login_t_name': username})
