# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from master.models import T_user
from master.models import ResUsers
from master.models import ResPartner
from master.models import AccountInvoice, AccountInvoiceLine
from master.models import PaymentMode
from master.models import ResCurrency,ResProduct
from common import logout
from django import forms
from django.http import HttpResponseRedirect
import json
from django.db import connection, transaction


# ---财务管理/发票列表页面
def cwgl_invoice_list(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    if not username:
        return logout(req)

    paymodelist = PaymentMode.objects.all().values('id','name')
    return render_to_response('starmerx_cwgl/invoice_list.html', {'login_t_name': username,'paymodelist':paymodelist})

# ---财务管理/发票审核页面
def cwgl_invoice_sh(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    paymodelist = PaymentMode.objects.all().values('id', 'name')
    return render_to_response('starmerx_cwgl/invoice_sh.html', {'login_t_name': username,'paymodelist':paymodelist})

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
            'validate': "待审核",
            'open': "待支付",
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
            partner = ResPartner.objects.get(id=invoice_obj.partner_id).name
            dict1['partner'] = partner
        else:
            dict1['partner'] = ''
        if invoice_obj.date_invoice:
            dict1['date_invoice'] = invoice_obj.date_invoice.strftime('%Y-%m-%d')
        else:
            dict1['date_invoice'] = ''
        dict1['number'] = invoice_obj.number
        # 销售员
        if invoice_obj.user_id:
            user = ResUsers.objects.get(id=invoice_obj.user_id).partner_id
            userp = ResPartner.objects.get(id=user)
            dict1['user'] = userp.name
        else:
            dict1['user'] = ''
        # 付款方式
        if invoice_obj.payment_mode:
            payment = PaymentMode.objects.get(id=invoice_obj.payment_mode).name
            dict1['payment_mode'] = payment
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
            # lastacline = AccountInvoiceLine.objects.filter(product_id=lineitem.product_id).exclude(
            #     invoice__state__in=['draft', 'cancel']).order_by(
            #     '-create_date').first()
            # if lastacline:
            #     line_dict['price_last'] = float(lastacline.price_unit)
            # else:
            #     line_dict['price_last'] = "无数据"
            lastacline = ResProduct.objects.get(id=lineitem.product_id).last_purchase_price
            if lastacline and lastacline > 0:
                line_dict['price_last'] = float(lastacline)
            else:
                line_dict['price_last'] = "无数据"
            line_list.append(line_dict)
        dict1['product_list'] = line_list
        dict1['comment'] = invoice_obj.comment
        dict1['amount_tax'] = invoice_obj.amount_tax
        dict1['discount_amount'] = invoice_obj.discount_amount

    return render_to_response('starmerx_cwgl/invoice_info.html', {'invoice_obj': dict1})


# ---财务管理/发票列表获取数据
def get_invoice_list(req):

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
    account_objs = AccountInvoice.objects.filter(**filterdist).values('id','partner_id','date_invoice','number','user_id','payment_mode','date_due','origin','currency_id','residual','amount_untaxed','amount_total','state')

    # cursor = connection.cursor()
    # cursor.execute("SELECT count(0) FROM account_invoice where " + searchstr)
    # zongrowcount = cursor.fetchone()
    zongrowcount = account_objs.count()

    zongdict = {}
    list1 = []

    def state_help(argument):
        switcher = {
            'draft': "草稿",
            'validate': "待审核",
            'open': "待支付",
            'partPaid': "部分支付",
            'paid': "已付",
            'closed': "已结案",
            'cancel': "已取消",
        }
        return switcher.get(argument, "nothing")

    for acitem in account_objs[startjilu:endjilu]:
        dict1 = {}
        dict1['id'] = acitem['id']
        # 供应商
        if acitem['partner_id']:
            partner = ResPartner.objects.get(id=acitem['partner_id']).name
            dict1['partner'] = partner
        else:
            dict1['partner'] = ''
        if acitem['date_invoice']:
            dict1['date_invoice'] = acitem['date_invoice'].strftime('%Y-%m-%d')
        else:
            dict1['date_invoice'] = ''
        dict1['number'] = acitem['number']
        # 销售员
        if acitem['user_id']:
            user = ResUsers.objects.get(id=acitem['user_id']).partner_id
            userp = ResPartner.objects.get(id=user).name
            dict1['user'] = userp
        else:
            dict1['user'] = ''
        # 付款方式
        if acitem['payment_mode']:
            payment = PaymentMode.objects.get(id=acitem['payment_mode']).name
            dict1['payment_mode'] = payment
        else:
            dict1['payment_mode'] = ''
        if acitem['date_due']:
            dict1['date_due'] = acitem['date_due'].strftime('%Y-%m-%d')
        else:
            dict1['date_due'] = ''
        dict1['origin'] = acitem['origin']
        # 币种
        biz = ResCurrency.objects.get(id=acitem['currency_id'])
        dict1['currency'] = biz.name
        dict1['residual'] = float(acitem['residual'])
        # 小计
        dict1['amount_untaxed'] = float(acitem['amount_untaxed'])
        # 合计
        dict1['amount_total'] = float(acitem['amount_total'])

        dict1['state'] = state_help(acitem['state'])
        line_objs = AccountInvoiceLine.objects.filter(invoice_id=acitem['id']).values('name','quantity','price_unit','product_id')
        line_list = []
        for lineitem in line_objs:
            line_dict = {}
            line_dict['name'] = lineitem['name']
            line_dict['quantity'] = int(lineitem['quantity'])
            line_dict['price_unit'] = float(lineitem['price_unit'])
            # lastacline = AccountInvoiceLine.objects.filter(product_id=lineitem['product_id']).exclude(
            #     invoice__state__in=['draft', 'cancel']).order_by(
            #     '-create_date').first()
            # if lastacline:
            #     line_dict['price_last'] = float(lastacline.price_unit)
            # else:
            #     line_dict['price_last'] = "无数据"
            lastacline = ResProduct.objects.get(id=lineitem['product_id']).last_purchase_price
            if lastacline and lastacline > 0:
                line_dict['price_last'] = float(lastacline)
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
    # filterdist['state'] = 'draft'
    scpsign = False
    scpxsign = False
    if req.GET.has_key('paymode') and req.GET['paymode'] != "0":
        filterdist['payment_mode'] = req.GET['paymode']


    if req.GET.has_key('origin') and req.GET['origin'] != "":
        filterdist['origin'] = req.GET['origin']

    # =================第一次筛选
    account_objs = AccountInvoice.objects.filter(**filterdist).filter(state__in=['draft','validate']).order_by("-id").values('id','partner_id','date_invoice','number','user_id','payment_mode','date_due','origin','currency_id','residual','amount_untaxed','amount_total','state')

    # =================第一次筛选end
    if req.GET.has_key('scp') and req.GET['scp'] != "0":
        scpsign = True  # 筛选>上次采购价的百分比
        # searchstr += " and payment_mode=" + req.GET['paymode']
    if req.GET.has_key('scpx') and req.GET['scpx'] != "0":
        scpxsign = True  # 筛选《=上次采购价
        # searchstr += " and payment_mode=" + req.GET['paymode']
    if req.GET.has_key('amount_total') and req.GET['amount_total'] != "":
        account_objs = account_objs.filter(amount_total__lte=req.GET['amount_total'])
        print account_objs.filter(amount_total__lte=req.GET['amount_total']).query
    # zongrowcount = account_objs.count()
    zongrowcount = 0

    zongdict = {}
    list1 = []

    def state_help(argument):
        switcher = {
            'draft': "草稿",
            'validate': "待审核",
            'open': "待支付",
            'partPaid': "部分支付",
            'paid': "已付",
            'closed': "已结案",
            'cancel': "已取消",
        }
        return switcher.get(argument, "nothing")

    if scpxsign:
        for acitem in account_objs:
            dict1 = {}

            line_objs = AccountInvoiceLine.objects.filter(invoice_id=acitem['id']).values('name', 'quantity', 'price_unit',
                                                                                          'product_id')
            line_list = []
            oksign = True  # 本次采购价小于等于上次采购价标识
            ok1sign = True # 满足本分比标识
            for lineitem in line_objs:
                line_dict = {}
                line_dict['name'] = lineitem['name']
                line_dict['quantity'] = int(lineitem['quantity'])
                line_dict['price_unit'] = float(lineitem['price_unit'])
                # lastacline = AccountInvoiceLine.objects.filter(product_id=lineitem['product_id']).exclude(
                #     invoice__state__in=['draft', 'cancel']).order_by(
                #     '-create_date').first()
                # if lastacline:
                #     line_dict['price_last'] = float(lastacline.price_unit)
                # else:
                #     line_dict['price_last'] = "无数据"
                lastacline = ResProduct.objects.get(id=lineitem['product_id']).last_purchase_price
                if lastacline and lastacline > 0:
                    line_dict['price_last'] = float(lastacline)
                    if lineitem['product_id'] != 2475 and float(lastacline) < float(lineitem['price_unit']):
                        oksign = False
                    # if lineitem['product_id'] != 2475 and (float(lastacline) * req.GET['scp']) > float(lineitem['price_unit']):
                    #     ok1sign = False
                else:
                    line_dict['price_last'] = "无数据"
                    if lineitem['product_id'] != 2475:
                        oksign = False
                        ok1sign = False
                line_list.append(line_dict)
            if scpxsign:
                if oksign:
                    zongrowcount += 1
                    dict1['product_list'] = line_list
                    dict1['id'] = acitem['id']
                    # 供应商
                    if acitem['partner_id']:
                        partner = ResPartner.objects.get(id=acitem['partner_id']).name
                        dict1['partner'] = partner
                    else:
                        dict1['partner'] = ''
                    if acitem['date_invoice']:
                        dict1['date_invoice'] = acitem['date_invoice'].strftime('%Y-%m-%d')
                    else:
                        dict1['date_invoice'] = ''
                    dict1['number'] = acitem['number']
                    # 销售员
                    if acitem['user_id']:
                        user = ResUsers.objects.get(id=acitem['user_id']).partner_id
                        userp = ResPartner.objects.get(id=user).name
                        dict1['user'] = userp
                    else:
                        dict1['user'] = ''
                    # 付款方式
                    if acitem['payment_mode']:
                        payment = PaymentMode.objects.get(id=acitem['payment_mode']).name
                        dict1['payment_mode'] = payment
                    else:
                        dict1['payment_mode'] = ''
                    if acitem['date_due']:
                        dict1['date_due'] = acitem['date_due'].strftime('%Y-%m-%d')
                    else:
                        dict1['date_due'] = ''
                    dict1['origin'] = acitem['origin']
                    # 币种
                    biz = ResCurrency.objects.get(id=acitem['currency_id'])
                    dict1['currency'] = biz.name
                    dict1['residual'] = float(acitem['residual'])
                    # 小计
                    dict1['amount_untaxed'] = float(acitem['amount_untaxed'])
                    # 合计
                    dict1['amount_total'] = float(acitem['amount_total'])

                    dict1['state'] = state_help(acitem['state'])

                    list1.append(dict1)
                else:
                    pass

            else:
                zongrowcount += 1
                dict1['product_list'] = line_list
                dict1['id'] = acitem['id']
                # 供应商
                if acitem['partner_id']:
                    partner = ResPartner.objects.get(id=acitem['partner_id']).name
                    dict1['partner'] = partner
                else:
                    dict1['partner'] = ''
                if acitem['date_invoice']:
                    dict1['date_invoice'] = acitem['date_invoice'].strftime('%Y-%m-%d')
                else:
                    dict1['date_invoice'] = ''
                dict1['number'] = acitem['number']
                # 销售员
                if acitem['user_id']:
                    user = ResUsers.objects.get(id=acitem['user_id']).partner_id
                    userp = ResPartner.objects.get(id=user).name
                    dict1['user'] = userp
                else:
                    dict1['user'] = ''
                # 付款方式
                if acitem['payment_mode']:
                    payment = PaymentMode.objects.get(id=acitem['payment_mode']).name
                    dict1['payment_mode'] = payment
                else:
                    dict1['payment_mode'] = ''
                if acitem['date_due']:
                    dict1['date_due'] = acitem['date_due'].strftime('%Y-%m-%d')
                else:
                    dict1['date_due'] = ''
                dict1['origin'] = acitem['origin']
                # 币种
                biz = ResCurrency.objects.get(id=acitem['currency_id'])
                dict1['currency'] = biz.name
                dict1['residual'] = float(acitem['residual'])
                # 小计
                dict1['amount_untaxed'] = float(acitem['amount_untaxed'])
                # 合计
                dict1['amount_total'] = float(acitem['amount_total'])

                dict1['state'] = state_help(acitem['state'])

                list1.append(dict1)
        zongdict['total'] = zongrowcount
        # zongdict['zongpages'] = zongpages
        # zongdict['pageindex'] = pageindex
        zongdict['rows'] = list1[startjilu:endjilu]
    else:
        zongrowcount = account_objs.count()
        for acitem in account_objs[startjilu:endjilu]:
            dict1 = {}

            line_objs = AccountInvoiceLine.objects.filter(invoice_id=acitem['id']).values('name', 'quantity',
                                                                                          'price_unit',
                                                                                          'product_id')
            line_list = []
            oksign = True  # 本次采购价小于等于上次采购价标识
            ok1sign = True  # 满足本分比标识
            for lineitem in line_objs:
                line_dict = {}
                line_dict['name'] = lineitem['name']
                line_dict['quantity'] = int(lineitem['quantity'])
                line_dict['price_unit'] = float(lineitem['price_unit'])
                # lastacline = AccountInvoiceLine.objects.filter(product_id=lineitem['product_id']).exclude(
                #     invoice__state__in=['draft', 'cancel']).order_by(
                #     '-create_date').first()
                # if lastacline:
                #     line_dict['price_last'] = float(lastacline.price_unit)
                # else:
                #     line_dict['price_last'] = "无数据"
                lastacline = ResProduct.objects.get(id=lineitem['product_id']).last_purchase_price
                if lastacline and lastacline > 0:
                    line_dict['price_last'] = float(lastacline)
                    if lineitem['product_id'] != 2475 and float(lastacline) < float(lineitem['price_unit']):
                        oksign = False
                        # if lineitem['product_id'] != 2475 and (float(lastacline) * req.GET['scp']) > float(lineitem['price_unit']):
                        #     ok1sign = False
                else:
                    line_dict['price_last'] = "无数据"
                    if lineitem['product_id'] != 2475:
                        oksign = False
                        ok1sign = False
                line_list.append(line_dict)

            dict1['product_list'] = line_list
            dict1['id'] = acitem['id']
            # 供应商
            if acitem['partner_id']:
                partner = ResPartner.objects.get(id=acitem['partner_id']).name
                dict1['partner'] = partner
            else:
                dict1['partner'] = ''
            if acitem['date_invoice']:
                dict1['date_invoice'] = acitem['date_invoice'].strftime('%Y-%m-%d')
            else:
                dict1['date_invoice'] = ''
            dict1['number'] = acitem['number']
            # 销售员
            if acitem['user_id']:
                user = ResUsers.objects.get(id=acitem['user_id']).partner_id
                userp = ResPartner.objects.get(id=user).name
                dict1['user'] = userp
            else:
                dict1['user'] = ''
            # 付款方式
            if acitem['payment_mode']:
                payment = PaymentMode.objects.get(id=acitem['payment_mode']).name
                dict1['payment_mode'] = payment
            else:
                dict1['payment_mode'] = ''
            if acitem['date_due']:
                dict1['date_due'] = acitem['date_due'].strftime('%Y-%m-%d')
            else:
                dict1['date_due'] = ''
            dict1['origin'] = acitem['origin']
            # 币种
            biz = ResCurrency.objects.get(id=acitem['currency_id'])
            dict1['currency'] = biz.name
            dict1['residual'] = float(acitem['residual'])
            # 小计
            dict1['amount_untaxed'] = float(acitem['amount_untaxed'])
            # 合计
            dict1['amount_total'] = float(acitem['amount_total'])

            dict1['state'] = state_help(acitem['state'])

            list1.append(dict1)

        zongdict['total'] = zongrowcount
        # zongdict['zongpages'] = zongpages
        # zongdict['pageindex'] = pageindex
        zongdict['rows'] = list1
    return HttpResponse(json.dumps(zongdict), content_type="application/json")

# ---财务管理/发票确认逻辑 draft-validate
def make_invoice_validate(req):
    selids = None
    result = {'result':'no'}
    if req.is_ajax():
        selids = req.GET.getlist('selids[]')
        AccountInvoice.objects.filter(id__in=selids).update(state='validate')
        result['result'] = 'yes'
    return HttpResponse(json.dumps(result), content_type="application/json")

# ---财务管理/发票审核通过逻辑 validate--open
def make_invoice_validate1(req):
    selids = None
    result = {'result':'no'}
    if req.is_ajax():
        selids = req.GET.getlist('selids[]')
        AccountInvoice.objects.filter(id__in=selids).update(state='open')
        result['result'] = 'yes'
    return HttpResponse(json.dumps(result), content_type="application/json")

# ---财务管理/发票审核不通过逻辑 validate-draft
def make_invoice_validate2(req):
    selids = None
    result = {'result':'no'}
    if req.is_ajax():
        selids = req.GET.getlist('selids[]')
        AccountInvoice.objects.filter(id__in=selids).update(state='draft')
        result['result'] = 'yes'
    return HttpResponse(json.dumps(result), content_type="application/json")