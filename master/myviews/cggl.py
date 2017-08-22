# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from master.models import T_user
from master.models import ResUsers
from master.models import ResPartner
from master.models import AccountInvoice, AccountInvoiceLine
from master.models import PaymentMode
from master.models import PurchaseOrder, PurchaseOrderLine, ProductUom, StcokPicking, StcokMove,WkfInstance,WkfWorkitem
from master.models import ResCurrency, ResProduct, StockWareHouse, StarmerxInventory,ResProductTemplate,Purchase_Invoice_Rel
from common import logout
import datetime
import json
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response
import sys
from django.db import connection
from django.db import transaction
from django.utils import timezone
from datetime import date,timedelta
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# ---采购管理/询价单列表页面
def cggl_xjd_list(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)

    # paymodelist = PaymentMode.objects.all().values('id','name')
    # purchasers_list = ResPartner.objects.filter(supplier='f',user_id__isnull=True,customer ='f')
    # gys_list = ResPartner.objects.filter(supplier='t')
    return render_to_response('starmerx_cggl/xjd_list.html',
                              {'login_t_name': username})
    # return render_to_response('starmerx_cggl/xjd_list.html',
    #                           {'login_t_name': username, 'purchasers_list': purchasers_list, 'gys_list': gys_list})


# ---采购管理/询价单列表获取数据
def get_xjd_list(req):
    username = req.session.get('login_t_name', default=None)
    uid = req.session.get('login_t_id')
    if not username:
        return logout(req)
    order = 'desc'
    sort = 'create_date'
    limit = 20
    offset = 0
    if req.GET.has_key('sort'):
        sort = req.GET['sort']
        if sort == 'partner':
            sort = 'partner_id'
    if req.GET.has_key('order'):
        order = req.GET['order']
    if req.GET.has_key('limit'):
        limit = int(req.GET['limit'])
    if req.GET.has_key('offset'):
        offset = int(req.GET['offset'])
    startjilu = int(offset)
    endjilu = int(offset) + int(limit)
    filterdist = {}
    filterdist['state'] = 'draft'
    purchase_objs = PurchaseOrder.objects.filter(state='draft')
    # if req.GET.has_key('gys_qt') and req.GET['gys_qt'] != "0":
    #     filterdist['partner_id'] = req.GET['gys_qt']
    # if req.GET.has_key('purchaser_qt') and req.GET['purchaser_qt'] != "0":
    #     # purchaser_id 为user_id
    #     ru = ResUsers.objects.filter(partner_id=req.GET['purchaser_qt'])
    #     filterdist['purchaser_id'] = ru[0].id
    if req.GET.has_key('name_qt') and req.GET['name_qt'] != "":
        filterdist['name'] = req.GET['name_qt']
        purchase_objs = purchase_objs.filter(name__icontains=req.GET['name_qt'])
    if req.GET.has_key('partner_id') and req.GET['partner_id'] != "0":
        filterdist['partner_id'] = req.GET['partner_id']
        purchase_objs = purchase_objs.filter(partner_id=req.GET['partner_id'])
    if uid!=1 and uid!=214:  #214是罗杰的账户
        purchase_objs = purchase_objs.filter(purchaser_id=uid)
    # purchase_objs = PurchaseOrder.objects.filter(**filterdist).order_by('-id')
    orderby = ''
    if order == 'desc':
        orderby = '-' + sort
    else:
        orderby = sort
    purchase_objs = purchase_objs.order_by(orderby).values('id', 'name', 'date_order',
                                                           'create_date',
                                                           'partner_id', 'origin',
                                                           'amount_untaxed',
                                                           'amount_total', 'state',
                                                           'stock_state',
                                                           'partner_id','location_id')
    # cursor = connection.cursor()
    # cursor.execute("SELECT count(0) FROM account_invoice where " + searchstr)
    # zongrowcount = cursor.fetchone()
    zongrowcount = purchase_objs.count()

    zongdict = {}
    list1 = []

    def state_help(argument):
        switcher = {
            'draft': "草稿",
            'done': "完成",
            'cancel': "已取消",
            'approved': "采购订单",
            'except_picking': "运输异常",
        }
        return switcher.get(argument, "nothing")

    def stock_state_help(argument):
        switcher = {
            'done': '完成收货',
            'exception': '部分收货',
            'none': '无入库单',
            'assigned': '准备收货',
            'cancel': '取消收货',
            'receiving': '正在收货',
        }
        return switcher.get(argument, "nothing")

    for poitem in purchase_objs[startjilu:endjilu]:
        dict1 = {}
        dict1['id'] = poitem['id']
        dict1['name'] = poitem['name']
        dict1['date_order'] = poitem['date_order'].strftime('%Y-%m-%d')


        dict1['create_date'] = (poitem['create_date']+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        # create_date = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S.%f')

        location = StockWareHouse.objects.filter(lot_input_id=poitem["location_id"])
        if location:
            dict1['location'] = location[0].name
        else:
            dict1['location'] = ""
        # 供应商
        if poitem['partner_id']:
            partner = ResPartner.objects.get(id=poitem['partner_id'])
            dict1['partner'] = partner.name
            # 采购负责人
            if partner.user_id != None:
                puser = ResUsers.objects.get(id=partner.user_id)
                if puser != None:
                    dict1['purchaser'] = ResPartner.objects.get(id=puser.partner_id).name
                else:
                    dict1['purchaser'] = ''
            else:
                dict1['purchaser'] = ''
        else:
            dict1['partner'] = ''
            dict1['purchaser'] = ''

        dict1['origin'] = poitem['origin']
        if poitem['amount_untaxed']:
            dict1['amount_untaxed'] = float(poitem['amount_untaxed'])
        else:
            dict1['amount_untaxed'] = ''
        if poitem['amount_total']:
            dict1['amount_total'] = float(poitem['amount_total'])
        else:
            dict1['amount_total'] = ''
        dict1['state'] = state_help(poitem['state'])
        dict1['stock_state'] = stock_state_help(poitem['stock_state'])

        list1.append(dict1)
    zongdict['total'] = zongrowcount

    zongdict['rows'] = list1
    return HttpResponse(json.dumps(zongdict), content_type="application/json")


# ---采购管理/手工创建询价单
def purchase_order_add(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)

    now = datetime.now().strftime('%Y-%m-%d')
    stockwarehouselist = StockWareHouse.objects.filter(
        lot_input_id__in=[118, 135, 141, 146, 147, 171, 13, 16, 19,176]).values('lot_input_id', 'name')
    paymodelist = PaymentMode.objects.all().values('id', 'name')
    partnerlist = ResPartner.objects.filter(supplier='t').values('id', 'name')[0:10]
    # productlist = ResProduct.objects.filter(product_tmpl__type='product',product_tmpl__purchase_ok='t').values('id', 'name_template', 'last_purchase_price')[0:10]
    # print productlist.query
    productuomlist = ProductUom.objects.all().values('id', 'name')
    return render_to_response('starmerx_cggl/purchase_order_add.html',
                              {'login_t_name': username, 'productuomlist': productuomlist,
                               'partnerlist': partnerlist, 'paymodelist': paymodelist,
                               'warehouselist': stockwarehouselist, 'now': now})


# ---采购管理/采购订单列表
def purchase_order_list(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    if not username:
        return logout(req)

    # paymodelist = PaymentMode.objects.all().values('id','name')
    return render_to_response('starmerx_cggl/purchase_order_list.html', {'login_t_name': username})


# ---采购管理/创建询价单
def create_purchase_order(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    result = {'result': 'no'}
    # if req.GET.has_key('product_id') and req.GET['product_id'] != "0" and req.GET.has_key('price_unit') \
    #         and req.GET['price_unit'] != "0" and req.GET.has_key('product_qty') and req.GET['product_qty'] != "0" \
    #         and req.GET.has_key('product_uom') and req.GET['product_uom'] != "0":
    if req.GET.has_key('orderline') and req.GET.has_key('partner_id') and req.GET.has_key(
            'payment_mode') and req.GET.has_key('location_id') and req.GET.has_key('amount_total'):
        print req.GET['orderline']
        print eval(req.GET["orderline"])

        #验证供应商是否归属当前用户
        res_p = ResPartner.objects.get(id=req.GET['partner_id'])
        if res_p.user_id !=req.session.get('login_t_id'):
            result['result'] = u'所选择的供应商不在你的名下'
            return HttpResponse(json.dumps(result), content_type="application/json")
        # PurchaseOrderLine.objects.create(product_id=req.GET['product_id'],price_unit=req.GET['price_unit'],
        #                                  product_qty=req.GET['product_qty'],product_uom=req.GET['product_uom'],order_id=100,name=pname,date_planned='2017-07-07',state='draft')
        name = "PO" + datetime.now().strftime('%Y%m%d')[2:] + str(
            int(PurchaseOrder.objects.all().order_by("-id")[0].name.split('_')[0][8:]) + 1) + "_wms"
        new_name = "PO" + datetime.now().strftime('%Y%m%d%H%M%S')[2:] + "_wms"
        # 创建的PO默认pricelist_id=2 是人民币，写死。后期需要可修改逻辑

        create_uid = req.session.get('login_t_id')
        # create_date = (datetime.now()+timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S.%f')
        create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        date_order = datetime.now().strftime('%Y-%m-%d')
        purchaser_id = 0
        rp = ResPartner.objects.get(id=req.GET['partner_id'])
        purchaser_id = rp.user_id
        po = PurchaseOrder.objects.create(create_date=create_date, create_uid=create_uid, name=new_name, origin='OP',
                                          partner_id=req.GET['partner_id'], location_id=req.GET['location_id'],warehouse_id=1,
                                          pricelist_id=2, date_order=date_order, company_id=1,
                                          partner_ref=req.GET['partner_ref'], payment_mode=req.GET['payment_mode'],
                                          logistics_company=req.GET['logistics_company'],
                                          track_number=req.GET['track_number'],
                                          notes=req.GET['notes'], amount_total=req.GET['amount_total'], state='draft',
                                          invoice_method='manual', stock_state='none', purchaser_id=purchaser_id
                                          )
        print po.id
        # 写ERP工作流表
        wks_ins_p_o = WkfInstance.objects.create(wkf_id=5, uid=1, res_type='purchase.order', state='active',
                                                 res_id=po.id)
        WkfWorkitem.objects.create(act_id=26, inst_id=wks_ins_p_o.id, state='complete')
        # 写采购明细====================================
        # 写一条运费
        PurchaseOrderLine.objects.create(create_date=create_date, create_uid=create_uid,
                                         product_id=2475, price_unit=0,
                                         product_qty=1,company_id=1,
                                         should_purchase_qty_real=1,
                                         product_uom=1,partner_id=req.GET['partner_id'],
                                         order_id=po.id, name='运费', date_planned=date_order, state='draft')
        orderlineList = eval(req.GET["orderline"])
        for orderline in orderlineList:
            product = ResProduct.objects.get(id=orderline['product_id'])
            pname = "[" + product.default_code + "]" + product.name_template
            PurchaseOrderLine.objects.create(create_date=create_date, create_uid=create_uid,
                                             product_id=orderline["product_id"], price_unit=orderline['price_unit'],
                                             product_qty=orderline['product_qty'],
                                             should_purchase_qty_real=orderline['product_qty'],
                                             product_uom=1,company_id=1,partner_id=req.GET['partner_id'],
                                             order_id=po.id, name=pname, date_planned=date_order, state='draft',
                                             last_supplier=product.last_supplier,last_purchase_price=product.last_purchase_price)
            # 增加在途库存
            Vinventory = StarmerxInventory.objects.filter(product_id=orderline["product_id"], type='virtual',
                                                          location_id=req.GET['location_id'])
            if Vinventory.count() > 0:
                old_stock_qty = Vinventory[0].stock_qty
                Vinventory.update(stock_qty=old_stock_qty + int(orderline['product_qty']))
            else:
                StarmerxInventory.objects.create(create_date=create_date, create_uid=create_uid, type='virtual',
                                                 stock_qty=int(orderline['product_qty']), usable_qty=0, state='enabled',
                                                 location_id=req.GET['location_id'], product_id=orderline["product_id"],
                                                 is_lock='f')
        result['result'] = 'yes'
        result['POID'] = po.id

    return HttpResponse(json.dumps(result), content_type="application/json")


# ---采购管理/采购订单明细页面
def purchase_order_info(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)

    def invoice_state_help(argument):
        switcher = {
            'draft': '草稿',
            'validate': 'validate',
            'open': '待支付',
            'partPaid': '部分支付',
            'paid': '已支付',
            'cancel': '已取消',
        }
        return switcher.get(argument, "nothing")

    purchase_order_obj = PurchaseOrder.objects.get(id=req.GET['poid'])
    title = ''
    reason = 0
    if purchase_order_obj.state == 'draft':
        title = '询价单'
        reason = 1
    elif purchase_order_obj.state == 'cancel':
        title = '已取消的询价单'
        reason = 0
    else:
        title = '采购单'
        reason = 10
    dict1 = {}
    if purchase_order_obj.partner_id:
        partner = ResPartner.objects.get(id=purchase_order_obj.partner_id)
        if partner:
            dict1["partner"] = partner.name
        else:
            dict1["partner"] = ""
    else:
        dict1["partner"] = ""
    if purchase_order_obj.payment_mode:
        paymode = PaymentMode.objects.get(id=purchase_order_obj.payment_mode)
        if paymode:
            dict1["paymode"] = paymode.name
        else:
            dict1["paymode"] = ""
    else:
        dict1["paymode"] = ""
    if purchase_order_obj.location_id:
        location = StockWareHouse.objects.filter(lot_input_id=purchase_order_obj.location_id)
        if location:
            dict1["location"] = location[0].name
        else:
            dict1["location"] = ""
    else:
        dict1["location"] = ""
    if purchase_order_obj.invoice_method == 'manual':
        dict1["invoice_method"] = "基于采购单明细"
    elif purchase_order_obj.invoice_method == 'picking':
        dict1["invoice_method"] = "基于收货量"
    elif purchase_order_obj.invoice_method == 'order':
        dict1["invoice_method"] = "基于生成的发票草稿"
    # 获取发票状态
    accountobj = AccountInvoice.objects.filter(name=purchase_order_obj.name)
    if accountobj:
        dict1['account_state'] = invoice_state_help(accountobj[0].state)
    else:
        dict1['account_state'] = ''
    # 获取预计到货时间
    if purchase_order_obj.minimum_planned_date == None or purchase_order_obj.minimum_planned_date == "":
        dict1['minimum_planned_date'] = ''
    else:
        dict1['minimum_planned_date'] = purchase_order_obj.minimum_planned_date.strftime('%Y-%m-%d')
    order_line_list = PurchaseOrderLine.objects.filter(order_id=purchase_order_obj.id)
    line_list = []
    for orderline in order_line_list:
        line_dict = {}
        line_dict["name"] = orderline.name
        line_dict["product_qty"] = orderline.product_qty
        line_dict["price_unit"] = orderline.price_unit
        # 获取单位
        # line_dict["uom_name"] = ProductUom.objects.get(id=orderline.product_uom).name
        line_dict["xj"] = orderline.product_qty * orderline.price_unit
        product = ResProduct.objects.get(id=orderline.product_id)

        line_dict["name"] = "["+product.default_code+"]"+product.name_template

        if reason==10:
            line_dict["last_purchase_price"] = orderline.last_purchase_price
            if orderline.last_supplier > 0:
                lp = ResPartner.objects.get(id=orderline.last_supplier)
                line_dict["last_supplier"] = lp.name
            else:
                line_dict["last_supplier"] = ""
        else:
            line_dict["last_purchase_price"] = product.last_purchase_price
            if product.last_supplier > 0:
                lp = ResPartner.objects.get(id=product.last_supplier)
                line_dict["last_supplier"] = lp.name
            else:
                line_dict["last_supplier"] = ""

        # 应采购数量
        line_dict["should_purchase_qty_real"] = orderline.should_purchase_qty_real
        line_dict["stockin_qty"] = orderline.stockin_qty

        # 获取备货人
        if orderline.person_stock_id >0:
            line_dict["bhr"] = ResPartner.objects.get(id=ResUsers.objects.get(id=orderline.person_stock_id).partner_id).name
        else:
            line_dict["bhr"] = ""
        line_list.append(line_dict)
    now = purchase_order_obj.create_date.strftime('%Y-%m-%d')
    return render_to_response('starmerx_cggl/purchase_order_info.html',
                              {'purchase_order_obj': purchase_order_obj, 'otherdata': dict1,
                               'order_line_list': line_list, 'title': title, 'reason': reason,'now':now})


# ---采购管理/采购单单列表获取数据
def get_purchase_order_list(req):
    username = req.session.get('login_t_name', default=None)
    uid = req.session.get('login_t_id')
    if not username:
        return logout(req)
    order = 'desc'
    limit = 20
    offset = 0
    sort= 'create_date'
    if req.GET.has_key('sort'):
        sort = req.GET['sort']
        if sort == 'partner':
            sort = 'partner_id'
    if req.GET.has_key('order'):
        order = req.GET['order']
    if req.GET.has_key('limit'):
        limit = int(req.GET['limit'])
    if req.GET.has_key('offset'):
        offset = int(req.GET['offset'])
    startjilu = int(offset)
    endjilu = int(offset) + int(limit)
    filterdist = {}

    purchase_objs = PurchaseOrder.objects.filter().exclude(state='draft')
    if req.GET.has_key('name_qt') and req.GET['name_qt'] != "":
        filterdist['name'] = req.GET['name_qt']
        purchase_objs = purchase_objs.filter(name__icontains=req.GET['name_qt'])
    if req.GET.has_key('partner_id') and req.GET['partner_id'] != "0":
        filterdist['partner_id'] = req.GET['partner_id']
        purchase_objs = purchase_objs.filter(partner_id=req.GET['partner_id'])
    if uid!=1 and uid!=214:  #214是罗杰的账户
        purchase_objs = purchase_objs.filter(purchaser_id=uid)
    orderby = ''
    if order == 'desc':
        orderby = '-' + sort
    else:
        orderby = sort

    purchase_objs = purchase_objs.order_by(orderby).values('id',
                                                           'name',
                                                           'date_order',
                                                           'create_date',
                                                           'partner_id',
                                                           'origin',
                                                           'amount_untaxed',
                                                           'amount_total',
                                                           'state',
                                                           'stock_state',
                                                           'partner_id','location_id')

    # cursor = connection.cursor()
    # cursor.execute("SELECT count(0) FROM account_invoice where " + searchstr)
    # zongrowcount = cursor.fetchone()
    zongrowcount = purchase_objs.count()

    zongdict = {}
    list1 = []

    def state_help(argument):
        switcher = {
            'draft': "草稿",
            'done': "完成",
            'cancel': "已取消",
            'approved': "采购订单",
            'except_picking': "运输异常",
        }
        return switcher.get(argument, "nothing")

    def stock_state_help(argument):
        switcher = {
            'done': '完成收货',
            'exception': '部分收货',
            'none': '无入库单',
            'assigned': '准备收货',
            'cancel': '取消收货',
            'receiving': '正在收货',
        }
        return switcher.get(argument, "nothing")

    def invoice_state_help(argument):
        switcher = {
            'draft': '草稿',
            'validate': 'validate',
            'open': '待支付',
            'partPaid': '部分支付',
            'paid': '已支付',
            'cancel': '已取消',
        }
        return switcher.get(argument, "nothing")

    for poitem in purchase_objs[startjilu:endjilu]:
        dict1 = {}
        dict1['id'] = poitem['id']
        dict1['name'] = poitem['name']
        dict1['date_order'] = poitem['date_order'].strftime('%Y-%m-%d')
        # dict1['create_date'] = poitem['create_date'].strftime('%Y-%m-%d %H:%M:%S')
        dict1['create_date'] = (poitem['create_date'] + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        location = StockWareHouse.objects.filter(lot_input_id=poitem["location_id"])
        if location:
            dict1['location'] = location[0].name
        else:
            dict1['location'] = ""
            # 供应商
        if poitem['partner_id']:
            partner = ResPartner.objects.get(id=poitem['partner_id'])
            dict1['partner'] = partner.name
            # 采购负责人
            if partner.user_id != None:
                puser = ResUsers.objects.get(id=partner.user_id)
                if puser != None:
                    dict1['purchaser'] = ResPartner.objects.get(id=puser.partner_id).name
                else:
                    dict1['purchaser'] = ''
            else:
                dict1['purchaser'] = ''
        else:
            dict1['partner'] = ''
            dict1['purchaser'] = ''

        dict1['origin'] = poitem['origin']
        if poitem['amount_untaxed']:
            dict1['amount_untaxed'] = float(poitem['amount_untaxed'])
        else:
            dict1['amount_untaxed'] = ''
        if poitem['amount_total']:
            dict1['amount_total'] = float(poitem['amount_total'])
        else:
            dict1['amount_total'] = ''
        dict1['state'] = state_help(poitem['state'])
        dict1['stock_state'] = stock_state_help(poitem['stock_state'])
        # 获取发票状态
        accountobj = AccountInvoice.objects.filter(origin__icontains=poitem['name'])
        if accountobj:
            dict1['account_state'] = invoice_state_help(accountobj[0].state)
        else:
            dict1['account_state'] = ''
        list1.append(dict1)
    zongdict['total'] = zongrowcount

    zongdict['rows'] = list1
    return HttpResponse(json.dumps(zongdict), content_type="application/json")


# ---采购管理/取消询价单
def cancel_purchase_order(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    result = {'result': 'no'}
    purchase_order_obj = PurchaseOrder.objects.filter(id=req.GET['poid'])
    purchase_order_obj.update(state='cancel', reason=req.GET['reason'])
    purchase_order_line_list = PurchaseOrderLine.objects.filter(order_id=req.GET['poid'])
    for line in purchase_order_line_list:
        # 减少在途
        Vinventory = StarmerxInventory.objects.filter(product_id=line.product_id, type='virtual',
                                                      location_id=purchase_order_obj[0].location_id)
        if Vinventory.count() > 0 and Vinventory[0].stock_qty - line.product_qty >= 0:
            Vinventory.update(stock_qty=Vinventory[0].stock_qty - line.product_qty)
    result['result'] = 'yes'
    result['POID'] = purchase_order_obj[0].id

    return HttpResponse(json.dumps(result), content_type="application/json")


# ---采购管理/合并询价单
def HB_purchase_order(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    result = {'result': 'no'}
    print req.GET['hbids']
    print eval(req.GET['hbids'])
    origin = ""
    partner_id = 0
    location_id = 0
    partner_ref = ""
    payment_mode = 0
    logistics_company = ""
    track_number = ""
    notes = ""
    amount_total = 0.0
    old_order_list = PurchaseOrder.objects.filter(id__in=eval(req.GET['hbids']))
    # 检测目标仓库
    old_loca = old_order_list[0].location_id
    kehb = True
    localist = {}
    # localist[old_locaname]=[old_order_list[0].name]
    for oldo in old_order_list:
        localist[oldo.name] =oldo.location_id
        if old_loca!=oldo.location_id:
            kehb = False

    if kehb==False:
        result['result'] = '合并的订单中存在目标仓库不一致的订单，请检查:'+str(localist)
        return HttpResponse(json.dumps(result), content_type="application/json")
    # 取消原来的询价单
    old_order_list.update(state='cancel')
    for oldorder in old_order_list:
        if oldorder.origin != None:
            origin += oldorder.origin
        amount_total += float(oldorder.amount_total)
    notes =""
    partner_ref = old_order_list[0].partner_ref
    logistics_company = ""
    track_number = ""
    partner_id = old_order_list[0].partner_id
    purchaser_id = old_order_list[0].purchaser_id
    location_id = old_order_list[0].location_id
    payment_mode = old_order_list[0].payment_mode

    # name = "PO" + datetime.now().strftime('%Y%m%d')[2:] + str(
    #     int(PurchaseOrder.objects.all().order_by("-id")[0].name.split('_')[0][8:]) + 1) + "_wms"

    new_name = "PO" + datetime.now().strftime('%Y%m%d%H%M%S')[2:] + "_wms"
    # 创建的PO默认pricelist_id=2 是人民币，写死。后期需要可修改逻辑
    create_uid = req.session.get('login_t_id')
    # create_date = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S.%f')
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    date_order = datetime.now().strftime('%Y-%m-%d')
    po = PurchaseOrder.objects.create(create_date=create_date, create_uid=create_uid, name=new_name, origin=origin,
                                      partner_id=partner_id, location_id=location_id,warehouse_id=1,
                                      pricelist_id=2, date_order=date_order, company_id=1,
                                      partner_ref=partner_ref, payment_mode=payment_mode,
                                      logistics_company=logistics_company,
                                      track_number=track_number,
                                      notes=notes, amount_total=amount_total, state='draft',
                                      invoice_method='manual', stock_state='none',purchaser_id=purchaser_id
                                      )
    print po.id
    # 写ERP工作流表
    wks_ins_p_o = WkfInstance.objects.create(wkf_id=5, uid=1, res_type='purchase.order', state='active',
                                                       res_id=po.id)
    WkfWorkitem.objects.create(act_id=26, inst_id=wks_ins_p_o.id, state='complete')
    # 写采购明细
    orderlinelist = PurchaseOrderLine.objects.filter(order_id__in=eval(req.GET['hbids']))
    pdict = {}
    for orderline in orderlinelist:
        if pdict.has_key(orderline.product_id) and orderline.product_id != 2475:
            # 有重复的sku
            sumcount = pdict[orderline.product_id][0] + orderline.product_qty
            PurchaseOrderLine.objects.filter(id=pdict[orderline.product_id][1]).update(product_qty=sumcount)
            pdict[orderline.product_id] = [sumcount, pdict[orderline.product_id][1]]
            PurchaseOrderLine.objects.create(create_date=create_date, create_uid=create_uid,person_stock_id=orderline.person_stock_id,
                                             product_id=orderline.product_id, price_unit=orderline.price_unit,
                                             product_qty=0, product_uom=1,company_id=1,partner_id=partner_id,
                                             order_id=po.id, name=orderline.name, date_planned=date_order,
                                             state='draft', move_dest_id=orderline.move_dest_id,
                                             should_purchase_qty_real=orderline.product_qty)

            continue
        elif orderline.product_id == 2475:
            pass
        else:
            pl = PurchaseOrderLine.objects.create(create_date=create_date, create_uid=create_uid,company_id=1,
                                                  product_id=orderline.product_id, price_unit=orderline.price_unit,
                                                  product_qty=orderline.product_qty, product_uom=1,partner_id=partner_id,
                                                  order_id=po.id, name=orderline.name, date_planned=date_order,
                                                  state='draft', move_dest_id=orderline.move_dest_id,person_stock_id=orderline.person_stock_id,
                                                  should_purchase_qty_real=orderline.product_qty)
            pdict[orderline.product_id] = [pl.product_qty, pl.id]

    # 写一条运费
    PurchaseOrderLine.objects.create(create_date=create_date, create_uid=create_uid,
                                     product_id=2475, price_unit=0,
                                     product_qty=1,company_id=1,
                                     should_purchase_qty_real=1,
                                     product_uom=1,partner_id=partner_id,
                                     order_id=po.id, name='运费', date_planned=date_order, state='draft')

    result['result'] = 'yes'

    return HttpResponse(json.dumps(result), content_type="application/json")


# ---采购管理/确认询价单为采购订单
def confirmed_purchase_order(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    result = {'result': '出错了'}
    purchase_order_obj = PurchaseOrder.objects.filter(id=req.GET['poid'])
    order_lines = PurchaseOrderLine.objects.filter(order_id=purchase_order_obj[0].id)
    kcg = True
    for order_line in order_lines:
        # 判断sku是否可采购
        if order_line.product_id != 2475:
            product = ResProduct.objects.get(id=order_line.product_id)
            product_template = ResProductTemplate.objects.get(id=product.product_tmpl_id)
            if product_template.purchase_ok !=True:
                kcg = False
                result = {'result': '采购明细中'+product.default_code+'不可采购，请核实'}
                return HttpResponse(json.dumps(result), content_type="application/json")
    if purchase_order_obj[0].location_id in [135, 141, 146, 147, 16, 19]:
        line_list = PurchaseOrderLine.objects.filter(order_id=purchase_order_obj[0].id)
        for line in line_list:
            if line.product_id != 2475 and line.person_stock_id == None:
                result = {'result': 'vip或西雅图仓必须要有备货人才能确认'}
                return HttpResponse(json.dumps(result), content_type="application/json")
    create_uid = req.session.get('login_t_id')
    # date_approve = (datetime.now()+ timedelta(hours=8)).strftime('%Y-%m-%d')
    # if datetime.now().hour>=12:
    #     date_approve = datetime.now().strftime('%Y-%m-%d')
    # else:
    #     date_approve = (datetime.now()+timedelta(day=1)).strftime('%Y-%m-%d')
    date_approve = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    date_order = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    purchase_order_line_list = PurchaseOrderLine.objects.filter(order_id=req.GET['poid'])
    #验证明sku是否存在数量为0并且价格为0的
    for line in purchase_order_line_list:
        if line.product_id !=2475 and line.product_qty>0 and line.price_unit<=0:
            result = {'result': '采购明细中有sku价格小于0的，不允许确认'}
            return HttpResponse(json.dumps(result), content_type="application/json")
    # 写stock_picking

    # name = "IN" + datetime.now().strftime('%Y%m%d')[2:] + str(
    #     int(StcokPicking.objects.filter(name__contains='IN').order_by("-id")[0].name.split('_')[0][8:]) + 1) + "_wms"
    new_name = "IN" + datetime.now().strftime('%Y%m%d%H%M%S%f')[2:] + "_wms"

    invoice_state = 'none'
    if purchase_order_obj[0].invoice_method == 'picking':
        invoice_state = '2binvoiced'
    spicking = StcokPicking.objects.create(create_date=create_date, create_uid=create_uid, date=date_order,
                                           company_id=1,name=new_name,
                                           origin=purchase_order_obj[0].name,
                                           partner_id=purchase_order_obj[0].partner_id, move_type='direct',
                                           invoice_state=invoice_state, state='assigned',
                                           location_dest_id=purchase_order_obj[0].location_id, auto_picking='f',
                                           type='in', purchase_id=purchase_order_obj[0].id, weight_uom_id=3)

    # 写ERP工作流表
    wks_ins_stock_picking = WkfInstance.objects.create(wkf_id=3,uid=1,res_type='stock.picking',state='active',res_id=spicking.id)
    WkfWorkitem.objects.create(act_id=12,inst_id=wks_ins_stock_picking.id,state='complete')
    # 更新询价单的工作流
    wkfinsobj = WkfInstance.objects.filter(res_type='purchase.order',res_id=purchase_order_obj[0].id)
    WkfWorkitem.objects.filter(inst_id=wkfinsobj[0].id).update(act_id=36,subflow_id=wks_ins_stock_picking.id,state='running')
    # 写发票(只有基于采购明细才生成发票)
    invoicelist = AccountInvoice.objects.filter(name=purchase_order_obj[0].name)
    if purchase_order_obj[0].invoice_method == 'manual' and invoicelist.count()<= 0:
        accountinv = AccountInvoice.objects.create(create_date=create_date, create_uid=create_uid,user_id=purchase_order_obj[0].purchaser_id,
                                                   origin=purchase_order_obj[0].name, currency_id=8, company_id=1,
                                                   partner_id=purchase_order_obj[0].partner_id, state='draft',
                                                   amount_untaxed=purchase_order_obj[0].amount_total,
                                                   amount_total=purchase_order_obj[0].amount_total, reconciled='f',
                                                   type='in_invoice', sent='f',
                                                   payment_mode=purchase_order_obj[0].payment_mode,comment=purchase_order_obj[0].notes,
                                                   name=purchase_order_obj[0].name, account_id=49, journal_id=2,reference_type='none')
        # 工作流
        wks_ins_account_invoice = WkfInstance.objects.create(wkf_id=1, uid=1, res_type='account.invoice', state='active',
                                                         res_id=accountinv.id)
        WkfWorkitem.objects.create(act_id=1, inst_id=wks_ins_account_invoice.id, state='complete')
        # 添加发票和采购单的关联
        # cursor = connection.cursor()
        # cursor.execute("SELECT count(0) FROM account_invoice where " + searchstr)
        # zongrowcount = cursor.fetchone()

        sql = 'insert into purchase_invoice_rel(purchase_id,invoice_id)values(%s,%s)'
        cursor = connection.cursor()
        cursor.execute(sql, [purchase_order_obj[0].id, accountinv.id])
        connection.commit()
        # Purchase_Invoice_Rel.objects.create(purchase_id=purchase_order_obj[0].id,invoice_id=accountinv.id)
    for line in purchase_order_line_list:
        # 写move
        if line.product_id !=2475:
            # move
            product_obj = ResProduct.objects.get(id=line.product_id)
            StcokMove.objects.create(create_date=create_date, create_uid=create_uid, date=date_order,
                                     origin=purchase_order_obj[0].name, product_qty=line.product_qty, product_uom=1,
                                     price_unit=line.price_unit,weight=product_obj.product_tmpl.weight,weight_net=product_obj.product_tmpl.weight_net,
                                     partner_id=line.partner_id, name=line.name, company_id=1,
                                     product_id=line.product_id, state='assigned', picking_id=spicking.id, priority=1,
                                     location_dest_id=purchase_order_obj[0].location_id, auto_validate='f',
                                     purchase_line_id=line.id, date_expected=date_order, location_id=8, weight_uom_id=3)
            # 更新上次采购价、更新上次供应商
            if line.product_qty != 0:
                line.last_purchase_price=ResProduct.objects.filter(id=line.product_id)[0].last_purchase_price
                line.last_supplier=ResProduct.objects.filter(id=line.product_id)[0].last_supplier
                line.save()
                ResProduct.objects.filter(id=line.product_id).update(last_purchase_price=line.price_unit,last_supplier=line.partner_id)
        # 写发票明细
        if purchase_order_obj[0].invoice_method == 'manual':
            AccountInvoiceLine.objects.create(create_date=create_date, create_uid=create_uid,
                                              origin=purchase_order_obj[0].name, name=line.name, invoice_id=accountinv.id,
                                              price_unit=line.price_unit,
                                              price_subtotal=line.product_qty * line.price_unit, company_id=1,
                                              quantity=line.product_qty,
                                              partner_id=line.partner_id,
                                              product_id=line.product_id, account_id=15)


    # 更新order和orderline的状态  date_approve:审核日期
    purchase_order_obj.update(state='approved',date_approve=date_approve,stock_state='assigned',validator=create_uid)
    purchase_order_line_list.update(state='confirmed')



    result['result'] = 'yes'

    return HttpResponse(json.dumps(result), content_type="application/json")


# ---采购管理/询价单编辑页面
def edit_purchase_order(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)

    def invoice_state_help(argument):
        switcher = {
            'draft': '草稿',
            'validate': 'validate',
            'open': '待支付',
            'partPaid': '部分支付',
            'paid': '已支付',
            'cancel': '已取消',
        }
        return switcher.get(argument, "nothing")

    purchase_order_obj = PurchaseOrder.objects.get(id=req.GET['poid'])
    title = ''
    reason = 0
    if purchase_order_obj.state == 'draft':
        title = '询价单'
        reason = 1
    else:
        title = '采购单'
    dict1 = {}
    if purchase_order_obj.partner_id:
        partner = ResPartner.objects.get(id=purchase_order_obj.partner_id)
        if partner:
            dict1["partner"] = partner.name
        else:
            dict1["partner"] = ""
    else:
        dict1["partner"] = ""
    if purchase_order_obj.payment_mode:
        paymode = PaymentMode.objects.get(id=purchase_order_obj.payment_mode)
        if paymode:
            dict1["paymode"] = paymode.name
        else:
            dict1["paymode"] = ""
    else:
        dict1["paymode"] = ""
    if purchase_order_obj.location_id:
        location = StockWareHouse.objects.filter(lot_input_id=purchase_order_obj.location_id)
        if location:
            dict1["location"] = location[0].name
        else:
            dict1["location"] = ""
    else:
        dict1["location"] = ""

    # 获取发票状态
    accountobj = AccountInvoice.objects.filter(name=purchase_order_obj.name)
    if accountobj:
        dict1['account_state'] = invoice_state_help(accountobj[0].state)
    else:
        dict1['account_state'] = ''
    # 获取预计到货时间
    if purchase_order_obj.minimum_planned_date == None or purchase_order_obj.minimum_planned_date == "":
        dict1['minimum_planned_date'] = ''
    else:
        dict1['minimum_planned_date'] = purchase_order_obj.minimum_planned_date.strftime('%Y-%m-%d')

    order_line_list = PurchaseOrderLine.objects.filter(order_id=purchase_order_obj.id)
    line_list = []
    for orderline in order_line_list:
        line_dict = {}
        line_dict["name"] = orderline.name
        line_dict["id"] = orderline.id
        line_dict["product_qty"] = orderline.product_qty
        line_dict["product_id"] = orderline.product_id
        line_dict["price_unit"] = orderline.price_unit
        # 获取单位
        # line_dict["uom_name"] = ProductUom.objects.get(id=orderline.product_uom).name
        # line_dict["uom_id"] = orderline.product_uom
        line_dict["xj"] = orderline.product_qty * orderline.price_unit
        product = ResProduct.objects.get(id=orderline.product_id)

        line_dict["name"] = "[" + product.default_code + "]" + product.name_template
        if reason == 10:
            line_dict["last_purchase_price"] = orderline.last_purchase_price
            if orderline.last_supplier > 0:
                lp = ResPartner.objects.get(id=orderline.last_supplier)
                line_dict["last_supplier"] = lp.name
            else:
                line_dict["last_supplier"] = ""
        else:
            line_dict["last_purchase_price"] = product.last_purchase_price
            if product.last_supplier > 0:
                lp = ResPartner.objects.get(id=product.last_supplier)
                line_dict["last_supplier"] = lp.name
            else:
                line_dict["last_supplier"] = ""
        # 应采购数量
        line_dict["should_purchase_qty_real"] = orderline.should_purchase_qty_real
        line_dict["stockin_qty"] = orderline.stockin_qty
        line_dict["person_stock_id"] = orderline.person_stock_id

        # 获取备货人
        if orderline.person_stock_id == None:
            line_dict["bhr"] = ""
        else:
            ru = ResUsers.objects.get(id=orderline.person_stock_id)
            rp = ResPartner.objects.get(id=ru.partner_id)
            line_dict["bhr"] = rp.name

        line_list.append(line_dict)

    now = purchase_order_obj.create_date.strftime('%Y-%m-%d')
    stockwarehouselist = StockWareHouse.objects.filter(
        lot_input_id__in=[118, 135, 141, 146, 147, 171, 13, 16, 19,176]).values('lot_input_id', 'name')
    paymodelist = PaymentMode.objects.all().values('id', 'name')
    partnerlist = ResPartner.objects.filter(supplier='t').values('id', 'name')[0:10]
    # productlist = ResProduct.objects.filter(product_tmpl__type='product',product_tmpl__purchase_ok='t').values('id', 'name_template', 'last_purchase_price')[0:10]
    productuomlist = ProductUom.objects.all().values('id', 'name')

    return render_to_response('starmerx_cggl/edit_purchase_order.html',
                              {'purchase_order_obj': purchase_order_obj, 'otherdata': dict1,
                               'order_line_list': line_list, 'title': title, 'reason': reason, 'login_t_name': username,
                               'productuomlist': productuomlist,
                               'partnerlist': partnerlist, 'paymodelist': paymodelist,
                               'warehouselist': stockwarehouselist, 'now': now})


# ---采购管理/更新询价单
def update_purchase_order(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    result = {'result': 'no'}
    # if req.GET.has_key('product_id') and req.GET['product_id'] != "0" and req.GET.has_key('price_unit') \
    #         and req.GET['price_unit'] != "0" and req.GET.has_key('product_qty') and req.GET['product_qty'] != "0" \
    #         and req.GET.has_key('product_uom') and req.GET['product_uom'] != "0":
    purchase_order_obj = PurchaseOrder.objects.filter(id=req.GET['poid'])

    create_uid = req.session.get('login_t_id')
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    date_order = datetime.now().strftime('%Y-%m-%d')
    if req.GET.has_key('partner_id') and req.GET.has_key(
            'payment_mode') and req.GET.has_key('location_id') and req.GET.has_key('amount_total'):

        # 验证供应商是否归属当前用户
        res_p = ResPartner.objects.get(id=req.GET['partner_id'])
        if res_p.user_id != req.session.get('login_t_id'):
            result['result'] = u'所选择的供应商不在你的名下'
            return HttpResponse(json.dumps(result), content_type="application/json")
        purchaser_id = 0
        rp = ResPartner.objects.get(id=req.GET['partner_id'])
        purchaser_id = rp.user_id
        minindate = None
        if (req.GET['minimum_planned_date']).strip() != "":
            minindate = datetime.strptime(req.GET['minimum_planned_date']+" 08:00:00",'%Y-%m-%d %H:%M:%S')
        po = purchase_order_obj.update(partner_id=req.GET['partner_id'], location_id=req.GET['location_id'],
                                       partner_ref=req.GET['partner_ref'], payment_mode=req.GET['payment_mode'],
                                       logistics_company=req.GET['logistics_company'],
                                       track_number=req.GET['track_number'],
                                       notes=req.GET['notes'], amount_total=req.GET['amount_total'],
                                       invoice_method=req.GET['invoice_method'], purchaser_id=purchaser_id,
                                       minimum_planned_date=minindate
                                       )
        # 删掉源PO明细增加的虚拟库存
        purchase_order_line_list = PurchaseOrderLine.objects.filter(order_id=purchase_order_obj[0].id)
        for line in purchase_order_line_list:
            # 减少在途
            Vinventory = StarmerxInventory.objects.filter(product_id=line.product_id, type='virtual',
                                                          location_id=purchase_order_obj[0].location_id)
            if Vinventory.count() > 0 and Vinventory[0].stock_qty - line.product_qty >= 0:
                Vinventory.update(stock_qty=Vinventory[0].stock_qty - line.product_qty)

        # 删除原来的明细记录
        oldids = []
        oldplist = PurchaseOrderLine.objects.filter(order_id=purchase_order_obj[0].id).values('id')
        for i in oldplist:
            oldids.append(i)
        # 写采购明细
        orderlineList = eval(req.GET["orderline"])
        for orderline in orderlineList:
            product = ResProduct.objects.get(id=orderline['product_id'])
            pname = "[" + product.default_code + "]" + product.name_template
            person_stock_id = None
            if orderline['person_stock_id'] =="None":
                person_stock_id = None
            else:
                person_stock_id =orderline['person_stock_id']
            PurchaseOrderLine.objects.create(create_date=create_date, create_uid=create_uid,
                                             product_id=orderline["product_id"],company_id=1,
                                             price_unit=orderline['price_unit'],person_stock_id=person_stock_id,
                                             product_qty=int(orderline['product_qty']),
                                             should_purchase_qty_real=int(orderline['product_qty']),
                                             product_uom=1,partner_id=req.GET['partner_id'],
                                             order_id=purchase_order_obj[0].id, name=pname, date_planned=date_order,
                                             state='draft')
            # 增加在途库存

            Vinventory = StarmerxInventory.objects.filter(product_id=orderline["product_id"], type='virtual',
                                                          location_id=req.GET['location_id'])
            if Vinventory.count() > 0:
                old_stock_qty = Vinventory[0].stock_qty
                Vinventory.update(stock_qty=old_stock_qty + int(orderline['product_qty']))
            else:
                StarmerxInventory.objects.create(create_date=create_date, create_uid=create_uid, type='virtual',
                                                 stock_qty=int(orderline['product_qty']), usable_qty=0,
                                                 state='enabled',
                                                 location_id=req.GET['location_id'],
                                                 product_id=orderline["product_id"],
                                                 is_lock='f')
        # 删除原来的明细记录
        for i in oldids:
            PurchaseOrderLine.objects.get(id=i["id"]).delete()
        result['POID'] = purchase_order_obj[0].id
        result['result'] = 'yes'

    return HttpResponse(json.dumps(result), content_type="application/json")


# ---采购管理/将已取消询价单重新设为询价单
def reto_purchase_order(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)
    result = {'result': 'no'}

    purchase_order_obj = PurchaseOrder.objects.filter(id=req.GET['poid'])
    purchase_order_obj.update(state='draft',reason='')
    orderlineList = PurchaseOrderLine.objects.filter(order_id=purchase_order_obj[0].id)
    create_uid = req.session.get('login_t_id')
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    for orderline in orderlineList:
        # 增加在途库存
        Vinventory = StarmerxInventory.objects.filter(product_id=orderline.product_id, type='virtual',
                                                      location_id=purchase_order_obj[0].location_id)
        if Vinventory.count() > 0:
            old_stock_qty = Vinventory[0].stock_qty
            Vinventory.update(stock_qty=old_stock_qty + int(orderline.product_qty))
        else:
            StarmerxInventory.objects.create(create_date=create_date, create_uid=create_uid, type='virtual',
                                             stock_qty=int(orderline.product_qty), usable_qty=0, state='enabled',
                                             location_id=purchase_order_obj[0].location_id, product_id=orderline.product_id,
                                             is_lock='f')

        result['result'] = 'yes'
        result['POID'] = purchase_order_obj[0].id

    return HttpResponse(json.dumps(result), content_type="application/json")
