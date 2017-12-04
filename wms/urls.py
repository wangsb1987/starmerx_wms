#coding=utf-8
"""wms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url

# 登录、退出、主页、欢迎页、个人设置方法引用
from master.myviews import common
# 财务管理方法引用
from master.myviews import cwgl
# 采购管理方法引用
from master.myviews import cggl
# 仓库管理方法引用
from master.myviews import ckgl

from master.myviews.Amazon import test


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^index/$', index),
    # url(r'^index1/(?P<id>\d{2})/$', index1),    #P一定要大写
    # url(r'^index2/(?P<parm>\d{2})/$', index2),
    # ======登录、退出、主页、欢迎页、个人设置url
    url(r'^$', common.login),
    url(r'^login/$', common.login),
    url(r'^logout/$', common.logout),
    url(r'^mainform/$', common.mainform),
    url(r'^mainform/main/$', common.main),
    url(r'^profile/$', common.profile),
    url(r'^common/getProducts/$', common.getProducts),
    url(r'^common/getSupplier/$', common.getSupplier),
    # ======财务管理url
    url(r'^starmerx_cwgl/invoice_list/$', cwgl.cwgl_invoice_list),
    url(r'^starmerx_cwgl/invoice_sh/$', cwgl.cwgl_invoice_sh),
    url(r'^starmerx_cwgl/invoice_info/$', cwgl.cwgl_invoice_info),
    url(r'^starmerx_cwgl/get_invoice_list/$', cwgl.get_invoice_list),
    url(r'^starmerx_cwgl/get_invoice_sh/$', cwgl.get_invoice_sh),
    url(r'^starmerx_cwgl/make_invoice_validate/$', cwgl.make_invoice_validate),
    url(r'^starmerx_cwgl/make_invoice_validate1/$', cwgl.make_invoice_validate1),

    # ======采购管理url
    url(r'^starmerx_cggl/xjd_list/$', cggl.cggl_xjd_list),
    url(r'^starmerx_cggl/get_xjd_list/$', cggl.get_xjd_list),
    url(r'^starmerx_cggl/purchase_order_add/$', cggl.purchase_order_add),
    url(r'^starmerx_cggl/purchase_order_list/$', cggl.purchase_order_list),
    url(r'^starmerx_cggl/create_purchase_order/$', cggl.create_purchase_order),
    url(r'^starmerx_cggl/purchase_order_info/$', cggl.purchase_order_info),
    url(r'^starmerx_cggl/get_purchase_order_list/$', cggl.get_purchase_order_list),
    url(r'^starmerx_cggl/cancel_purchase_order/$', cggl.cancel_purchase_order),
    url(r'^starmerx_cggl/HB_purchase_order/$', cggl.HB_purchase_order),
    url(r'^starmerx_cggl/edit_purchase_order/$', cggl.edit_purchase_order),
    url(r'^starmerx_cggl/update_purchase_order/$', cggl.update_purchase_order),
    url(r'^starmerx_cggl/confirmed_purchase_order/$', cggl.confirmed_purchase_order),
    url(r'^starmerx_cggl/reto_purchase_order/$', cggl.reto_purchase_order),

    # ======仓库管理url
    url(r'^starmerx_ckgl/stock_picking_list/$', ckgl.ckgl_stock_picking_list),

    url(r'^aa/$', test.test),
    url(r'^bb/$', test.test1),
]
