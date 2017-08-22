# -*- coding: utf-8 -*-
import sys
from common import logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection
from django.db import transaction
from django.utils import timezone
from datetime import date,timedelta
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# ---仓库管理/入库列表页面
def ckgl_stock_picking_list(req):
    username = req.session.get('login_t_name', default=None)
    if not username:
        return logout(req)

    # paymodelist = PaymentMode.objects.all().values('id','name')
    # purchasers_list = ResPartner.objects.filter(supplier='f',user_id__isnull=True,customer ='f')
    # gys_list = ResPartner.objects.filter(supplier='t')
    return render_to_response('starmerx_ckgl/stock_picking_list.html',
                              {'login_t_name': username})
