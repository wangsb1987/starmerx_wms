# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class T_user(models.Model):
    t_name = models.CharField(max_length=20)
    t_username = models.CharField(max_length=20,default='')
    t_userpsw = models.CharField(max_length=20,default='')

class AccountInvoice(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=64, blank=True, null=True)
    date_due = models.DateField(blank=True, null=True)
    check_total = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    reference = models.CharField(max_length=64, blank=True, null=True)
    supplier_invoice_number = models.CharField(max_length=64, blank=True, null=True)
    number = models.CharField(max_length=64, blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    fiscal_position = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    partner_bank_id = models.IntegerField(blank=True, null=True)
    payment_term = models.IntegerField(blank=True, null=True)
    reference_type = models.CharField(max_length=200)
    journal_id = models.IntegerField(blank=True, null=True)
    amount_tax = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    internal_number = models.CharField(max_length=32, blank=True, null=True)
    reconciled = models.NullBooleanField()
    residual = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    move_name = models.CharField(max_length=64, blank=True, null=True)
    date_invoice = models.DateField(blank=True, null=True)
    period_id = models.IntegerField(blank=True, null=True)
    amount_untaxed = models.FloatField(blank=True, null=True)
    move_id = models.IntegerField(blank=True, null=True)
    amount_total = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    sent = models.NullBooleanField()
    section_id = models.IntegerField(blank=True, null=True)
    payment_mode = models.IntegerField(blank=True, null=True)
    stock_location = models.CharField(max_length=200, blank=True, null=True)
    stock_warehouse = models.CharField(max_length=200, blank=True, null=True)
    purchase_notes = models.TextField(blank=True, null=True)
    discount_amount = models.FloatField(blank=True, null=True)
    # zfb_dealno = models.CharField(max_length=50, blank=True, null=True)
    # zfb_orderno = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_invoice'

class AccountInvoiceLine(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    origin = models.CharField(max_length=256, blank=True, null=True)
    uos_id = models.IntegerField(blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    name = models.TextField()
    sequence = models.IntegerField(blank=True, null=True)
    # 发票明细关联发票主表
    invoice = models.ForeignKey(AccountInvoice)
    price_unit = models.FloatField()
    price_subtotal = models.FloatField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    account_analytic_id = models.IntegerField(blank=True, null=True)
    quantity = models.FloatField()
    partner_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_invoice_line'

class PaymentMode(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    journal = models.IntegerField()
    partner_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField()
    bank_id = models.IntegerField()
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'payment_mode'


class ResPartner(models.Model):
    name = models.CharField(max_length=128)
    lang = models.CharField(max_length=64, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    use_parent_address = models.NullBooleanField()
    active = models.NullBooleanField()
    street = models.CharField(max_length=128, blank=True, null=True)
    supplier = models.NullBooleanField()
    city = models.CharField(max_length=128, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    zip = models.CharField(max_length=24, blank=True, null=True)
    title = models.IntegerField(blank=True, null=True)
    function = models.CharField(max_length=128, blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    employee = models.NullBooleanField()
    type = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=240, blank=True, null=True)
    vat = models.CharField(max_length=32, blank=True, null=True)
    website = models.CharField(max_length=64, blank=True, null=True)
    fax = models.CharField(max_length=64, blank=True, null=True)
    street2 = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    credit_limit = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    tz = models.CharField(max_length=64, blank=True, null=True)
    customer = models.NullBooleanField()
    image_medium = models.BinaryField(blank=True, null=True)
    mobile = models.CharField(max_length=64, blank=True, null=True)
    ref = models.CharField(max_length=64, blank=True, null=True)
    image_small = models.BinaryField(blank=True, null=True)
    birthdate = models.CharField(max_length=64, blank=True, null=True)
    is_company = models.NullBooleanField()
    state_id = models.IntegerField(blank=True, null=True)
    notification_email_send = models.CharField(max_length=256, blank=True, null=True)
    opt_out = models.NullBooleanField()
    signup_type = models.CharField(max_length=256, blank=True, null=True)
    signup_expiration = models.DateTimeField(blank=True, null=True)
    signup_token = models.CharField(max_length=256, blank=True, null=True)
    last_reconciliation_date = models.DateTimeField(blank=True, null=True)
    debit_limit = models.FloatField(blank=True, null=True)
    section_id = models.IntegerField(blank=True, null=True)
    market_supplier = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'res_partner'


class ResUsers(models.Model):
    active = models.NullBooleanField()
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64, blank=True, null=True)
    company_id = models.IntegerField()
    partner_id = models.IntegerField()
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)
    login_date = models.DateField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    action_id = models.IntegerField(blank=True, null=True)
    alias_id = models.IntegerField()
    share = models.NullBooleanField()
    default_section_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'res_users'

class ResCurrency(models.Model):
    name = models.CharField(max_length=32)
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    rounding = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    symbol = models.CharField(max_length=4, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    base = models.NullBooleanField()
    active = models.NullBooleanField()
    position = models.CharField(max_length=20, blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'res_currency'

class ResProductTemplate(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    warranty = models.FloatField(blank=True, null=True)
    uos_id = models.IntegerField(blank=True, null=True)
    list_price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    weight_net = models.FloatField(blank=True, null=True)
    standard_price = models.FloatField(blank=True, null=True)
    mes_type = models.CharField(max_length=128,blank=True, null=True)
    uom_id = models.IntegerField(blank=True, null=True)
    description_purchase = models.TextField(blank=True, null=True)
    cost_method = models.CharField(max_length=128,blank=True, null=True)
    categ_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128,blank=True, null=True)
    uos_coeff = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    sale_ok = models.NullBooleanField()
    description_sale = models.TextField(blank=True, null=True)
    product_manager = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    produce_delay = models.FloatField(blank=True, null=True)
    uom_po_id = models.IntegerField(blank=True, null=True)
    rental = models.NullBooleanField()
    type = models.CharField(max_length=50,blank=True, null=True)
    loc_rack = models.CharField(max_length=16,blank=True, null=True)
    loc_row = models.CharField(max_length=16,blank=True, null=True)
    sale_delay = models.FloatField(blank=True, null=True)
    loc_case = models.CharField(max_length=16,blank=True, null=True)
    supply_method = models.CharField(max_length=128,blank=True, null=True)
    procure_method = models.CharField(max_length=128,blank=True, null=True)
    purchase_ok = models.NullBooleanField()
    loc_us_rack = models.CharField(max_length=16,blank=True, null=True)
    loc_us_row = models.CharField(max_length=16,blank=True, null=True)
    loc_gz_rack = models.CharField(max_length=16,blank=True, null=True)
    loc_gz_row = models.CharField(max_length=16,blank=True, null=True)
    loc_vip_row = models.CharField(max_length=16,blank=True, null=True)
    loc_sea_rack = models.CharField(max_length=16,blank=True, null=True)
    loc_vip_rack = models.CharField(max_length=16,blank=True, null=True)
    loc_sea_row = models.CharField(max_length=16,blank=True, null=True)
    his_row = models.CharField(max_length=16,blank=True, null=True)
    his_gz_row = models.CharField(max_length=16,blank=True, null=True)
    his_sea_row = models.CharField(max_length=16,blank=True, null=True)
    his_gz_rack = models.CharField(max_length=16,blank=True, null=True)
    his_rack = models.CharField(max_length=16,blank=True, null=True)
    his_us_row = models.CharField(max_length=16,blank=True, null=True)
    his_vip_row = models.CharField(max_length=16,blank=True, null=True)
    his_vip_rack = models.CharField(max_length=16,blank=True, null=True)
    his_us_rack = models.CharField(max_length=16,blank=True, null=True)
    his_sea_rack = models.IntegerField(blank=True, null=True)
    pro_liquid_type = models.IntegerField(blank=True, null=True)
    battery_type = models.IntegerField(blank=True, null=True)
    pro_battery_type = models.IntegerField(blank=True, null=True)
    liquid_type = models.IntegerField(blank=True, null=True)
    loc_csea_row = models.CharField(max_length=16,blank=True, null=True)
    his_gvip_rack = models.CharField(max_length=16,blank=True, null=True)
    his_csea_rack = models.CharField(max_length=16,blank=True, null=True)
    his_gvip_row = models.CharField(max_length=16,blank=True, null=True)
    loc_gvip_row = models.CharField(max_length=16,blank=True, null=True)
    loc_gvip_rack = models.CharField(max_length=16,blank=True, null=True)
    loc_csea_rack = models.CharField(max_length=16,blank=True, null=True)
    his_csea_row = models.CharField(max_length=16,blank=True, null=True)
    loc_cvip_row = models.CharField(max_length=16,blank=True, null=True)
    loc_cvip_rack = models.CharField(max_length=16,blank=True, null=True)
    his_cvip_rack = models.CharField(max_length=16,blank=True, null=True)
    his_cvip_row = models.CharField(max_length=16,blank=True, null=True)
    loc_chfc_row = models.CharField(max_length=16,blank=True, null=True)
    loc_chfc_rack = models.CharField(max_length=16,blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_template'


class ResProduct(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    color = models.IntegerField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    price_extra = models.FloatField(blank=True, null=True)
    default_code = models.CharField(max_length=64,blank=True, null=True)
    name_template = models.CharField(max_length=128,blank=True, null=True)
    active = models.NullBooleanField()
    variants = models.CharField(max_length=128,blank=True, null=True)
    image_medium = models.BinaryField(blank=True, null=True)
    image_small = models.BinaryField(blank=True, null=True)
    #外键关联tmplate表
    product_tmpl = models.ForeignKey(ResProductTemplate)
    price_margin = models.FloatField(blank=True, null=True)
    track_outgoing = models.NullBooleanField()
    track_incoming = models.NullBooleanField()
    valuation = models.CharField(max_length=128, blank=True, null=True)
    track_production = models.NullBooleanField()
    english_name = models.CharField(max_length=128, blank=True, null=True)
    hr_expense_ok = models.NullBooleanField()
    us_pack_id = models.IntegerField(blank=True, null=True)
    pack_id = models.IntegerField(blank=True, null=True)
    starmerx_price = models.FloatField(blank=True, null=True)
    last_week_sale_data = models.FloatField(blank=True, null=True)
    last_purchase_price = models.FloatField(blank=True, null=True)
    gz_pack_id = models.IntegerField(blank=True, null=True)
    last_mounth_sale_data = models.FloatField(blank=True, null=True)
    last_2week_sale_data = models.FloatField(blank=True, null=True)
    vip_pack_id = models.IntegerField(blank=True, null=True)
    sea_pack_id = models.IntegerField(blank=True, null=True)
    real_pack_id = models.IntegerField(blank=True, null=True)
    last_purchaser = models.IntegerField(blank=True, null=True)
    gvip_pack_id = models.IntegerField(blank=True, null=True)
    cvip_pack_id = models.IntegerField(blank=True, null=True)
    csea_pack_id = models.IntegerField(blank=True, null=True)
    chfc_pack_id = models.IntegerField(blank=True, null=True)
    last_supplier = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_product'

class PurchaseOrder(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    journal_id = models.IntegerField(blank=True, null=True)
    date_order = models.DateTimeField(blank=True, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    dest_address_id = models.IntegerField(blank=True, null=True)
    fiscal_position = models.IntegerField(blank=True, null=True)

    amount_untaxed = models.FloatField(blank=True, null=True)
    location_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    amount_tax = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=64)
    pricelist_id = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    payment_term_id = models.IntegerField(blank=True, null=True)
    partner_ref = models.CharField(max_length=64)
    date_approve = models.DateTimeField(blank=True, null=True)
    amount_total = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=64)
    notes = models.TextField(blank=True, null=True)
    invoice_method = models.CharField(max_length=64)

    shipped = models.NullBooleanField()
    validator = models.IntegerField(blank=True, null=True)
    minimum_planned_date = models.DateTimeField(blank=True, null=True)
    stock_state = models.CharField(max_length=64)
    payment_tools_id = models.IntegerField(blank=True, null=True)
    carrier_id = models.IntegerField(blank=True, null=True)
    payment_mode = models.IntegerField(blank=True, null=True)
    purchaser_id = models.IntegerField(blank=True, null=True)
    spot_buying = models.NullBooleanField()
    origin = models.CharField(max_length=64)
    shop_id = models.IntegerField(blank=True, null=True)

    reason = models.TextField(blank=True, null=True)
    exception_reason = models.TextField(blank=True, null=True)
    logistics_company = models.CharField(max_length=64)
    track_number = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'purchase_order'

class PurchaseOrderLine(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    product_uom = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    price_unit = models.FloatField(blank=True, null=True)
    move_dest_id = models.IntegerField(blank=True, null=True)
    product_qty = models.FloatField(blank=True, null=True)

    partner_id = models.IntegerField(blank=True, null=True)
    invoiced = models.NullBooleanField()
    name = models.CharField(blank=True, null=True,max_length=64)
    date_planned = models.DateTimeField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    state = models.CharField(blank=True, null=True,max_length=64)
    product_id = models.IntegerField(blank=True, null=True)
    account_analytic_id = models.IntegerField(blank=True, null=True)
    stock_in_date = models.DateTimeField(blank=True, null=True)
    stock_state = models.CharField(blank=True, null=True,max_length=64)
    location_id = models.IntegerField(blank=True, null=True)
    purchaser_id = models.IntegerField(blank=True, null=True)
    purchase_state = models.CharField(blank=True, null=True,max_length=64)
    should_purchase_qty_real = models.IntegerField(blank=True, null=True)

    person_stock_id = models.IntegerField(blank=True, null=True)
    product_code = models.CharField(max_length=64)
    merge_before_qty = models.IntegerField(blank=True, null=True)
    is_merge = models.CharField(max_length=64)
    stockin_qty = models.IntegerField(blank=True, null=True)
    invoice_repair_state = models.CharField(max_length=64)
    notes = models.TextField(blank=True, null=True)
    is_first = models.CharField(max_length=64)
    last_new_supplier = models.IntegerField(blank=True, null=True)
    last_purchase_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase_order_line'


class ProductUom(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    uom_type = models.CharField(blank=True, null=True,max_length=64)
    category_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True,max_length=64)
    rounding = models.FloatField(blank=True, null=True)
    factor = models.FloatField(blank=True, null=True)

    active = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'product_uom'

class ProductPriceList(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True,max_length=64)
    active = models.NullBooleanField()
    type = models.CharField(blank=True, null=True,max_length=64)
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_pricelist'

class StockWareHouse(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    lot_input_id = models.IntegerField(blank=True, null=True)
    lot_output_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True,max_length=128)
    lot_stock_id = models.IntegerField(blank=True, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    nation = models.CharField(blank=True, null=True,max_length=15)
    active = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'stock_warehouse'

class StarmerxInventory(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    type = models.CharField(blank=True, null=True,max_length=15)
    stock_qty = models.IntegerField(blank=True, null=True)
    last_out_date = models.DateTimeField(blank=True, null=True)
    usable_qty = models.IntegerField(blank=True, null=True)
    lock_qty = models.IntegerField(blank=True, null=True)
    first_in_by = models.IntegerField(blank=True, null=True)
    last_out_by = models.IntegerField(blank=True, null=True)
    state = models.CharField(blank=True, null=True,max_length=15)

    first_in_date = models.DateTimeField(blank=True, null=True)
    last_in_date = models.DateTimeField(blank=True, null=True)
    last_in_by = models.IntegerField(blank=True, null=True)
    location_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    stock_up_qty = models.IntegerField(blank=True, null=True)
    is_lock = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'starmerx_inventory'

class ProcurementOrder(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    product_uom = models.IntegerField(blank=True, null=True)
    product_uos_qty = models.FloatField(blank=True, null=True)
    procure_method = models.CharField(blank=True, null=True,max_length=15)
    product_qty = models.FloatField(blank=True, null=True)
    product_uos = models.IntegerField(blank=True, null=True)
    message = models.CharField(blank=True, null=True,max_length=124)
    location_id = models.IntegerField(blank=True, null=True)
    move_id = models.IntegerField(blank=True, null=True)

    note = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    date_planned = models.DateTimeField(blank=True, null=True)
    close_move = models.NullBooleanField()
    company_id = models.IntegerField(blank=True, null=True)
    date_close = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(blank=True, null=True, max_length=15)

    state = models.CharField(blank=True, null=True, max_length=15)
    product_id = models.IntegerField(blank=True, null=True)
    purchase_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    origin = models.CharField(blank=True, null=True, max_length=128)
    sale_id = models.IntegerField(blank=True, null=True)
    is_declare = models.CharField(blank=True, null=True, max_length=15)
    procurement_order_id = models.IntegerField(blank=True, null=True)
    stock_state = models.CharField(blank=True, null=True, max_length=15)
    stockin_qty = models.IntegerField(blank=True, null=True)
    stockin_date_group = models.CharField(blank=True, null=True, max_length=64)
    stockin_date = models.DateTimeField(blank=True, null=True)
    account_id = models.CharField(blank=True, null=True, max_length=64)
    asin = models.CharField(blank=True, null=True, max_length=128)

    is_first = models.CharField(blank=True, null=True, max_length=15)
    virtual_stockin_qty = models.IntegerField(blank=True, null=True)
    confirm_move_qty = models.IntegerField(blank=True, null=True)
    move_state = models.CharField(blank=True, null=True, max_length=15)
    confirm_move_qty_total = models.IntegerField(blank=True, null=True)
    this_confirm_qty = models.IntegerField(blank=True, null=True)
    this_confirm_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'procurement_order'

class StcokPicking(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    origin = models.CharField(blank=True, null=True, max_length=64)
    date_done = models.DateTimeField(blank=True, null=True)
    min_date = models.DateTimeField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    stock_journal_id = models.IntegerField(blank=True, null=True)
    backorder_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True,max_length=64)

    location_id = models.IntegerField(blank=True, null=True)
    move_type = models.CharField(blank=True, null=True, max_length=15)
    company_id = models.IntegerField(blank=True, null=True)
    invoice_state = models.CharField(blank=True, null=True, max_length=15)
    note = models.TextField(blank=True, null=True)
    state = models.CharField(blank=True, null=True, max_length=15)
    location_dest_id = models.IntegerField(blank=True, null=True)

    max_date = models.DateTimeField(blank=True, null=True)
    auto_picking = models.NullBooleanField()
    type = models.CharField(blank=True, null=True, max_length=15)
    purchase_id = models.IntegerField(blank=True, null=True)
    sale_id = models.IntegerField(blank=True, null=True)
    carrier_tracking_ref = models.CharField(blank=True, null=True, max_length=32)
    number_of_packages = models.IntegerField(blank=True, null=True)
    carrier_id = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    weight_uom_id = models.IntegerField(blank=True, null=True)
    weight_net = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    relation_id = models.CharField(blank=True, null=True, max_length=64)
    min_date_olive = models.DateTimeField(blank=True, null=True)

    is_declare = models.CharField(blank=True, null=True, max_length=15)
    return_reason = models.CharField(blank=True, null=True, max_length=128)
    delivery_number = models.CharField(blank=True, null=True, max_length=64)
    realweight = models.FloatField(blank=True, null=True)
    freight_status = models.CharField(blank=True, null=True, max_length=64)
    packdone_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_picking'

class StcokMove(models.Model):
    create_uid = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    write_date = models.DateTimeField(blank=True, null=True)
    write_uid = models.IntegerField(blank=True, null=True)
    origin = models.CharField(blank=True, null=True, max_length=64)
    product_uos_qty = models.FloatField(blank=True, null=True)
    date_expected = models.DateTimeField(blank=True, null=True)
    product_uom = models.IntegerField(blank=True, null=True)
    price_unit = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    prodlot_id = models.IntegerField(blank=True, null=True)
    move_dest_id = models.IntegerField(blank=True, null=True)

    product_qty = models.FloatField(blank=True, null=True)
    product_uos = models.IntegerField(blank=True, null=True)
    partner_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=64)
    note = models.TextField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    auto_validate = models.NullBooleanField()

    price_currency_id = models.IntegerField(blank=True, null=True)
    location_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    picking_id = models.IntegerField(blank=True, null=True)
    priority = models.CharField(blank=True, null=True, max_length=32)
    state = models.CharField(blank=True, null=True, max_length=32)
    location_dest_id = models.IntegerField(blank=True, null=True)
    tracking_id = models.IntegerField(blank=True, null=True)
    product_packaging = models.IntegerField(blank=True, null=True)
    purchase_line_id = models.IntegerField(blank=True, null=True)
    sale_line_id = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    weight_net = models.FloatField(blank=True, null=True)
    weight_uom_id = models.IntegerField(blank=True, null=True)

    partner_related_ids = models.IntegerField(blank=True, null=True)
    on_hand = models.FloatField(blank=True, null=True)
    forecasted_quantity = models.FloatField(blank=True, null=True)
    dange = models.FloatField(blank=True, null=True)
    qty_of_package = models.FloatField(blank=True, null=True)
    can_be_merged = models.NullBooleanField()
    validator = models.IntegerField(blank=True, null=True)
    procurement_order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_move'


class WkfInstance(models.Model):
    wkf_id = models.IntegerField(blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    res_id = models.IntegerField(blank=True, null=True)
    res_type = models.CharField(blank=True, null=True, max_length=64)
    state = models.CharField(blank=True, null=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'wkf_instance'

class WkfWorkitem(models.Model):
    act_id = models.IntegerField(blank=True, null=True)
    inst_id = models.IntegerField(blank=True, null=True)
    subflow_id = models.IntegerField(blank=True, null=True)
    state = models.CharField(blank=True, null=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'wkf_workitem'

class Purchase_Invoice_Rel(models.Model):
    purchase_id = models.IntegerField(blank=True, null=True)
    invoice_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase_invoice_rel'

class StarmerxInventoryWmsReport(models.Model):
    product_id = models.IntegerField(blank=True, null=True)         # 产品ID
    stock_qty = models.IntegerField(blank=True, null=True)       # 库存
    location_id = models.IntegerField(blank=True, null=True)       # 仓库ID
    type = models.CharField(blank=True, null=True, max_length=16)    # 类型
    report_date = models.DateField(blank=True, null=True)           # 时间

    class Meta:
        managed = False
        db_table = 'starmerx_inventory_wms_report'


class StockMoveWmsReport(models.Model):
    wms_inventory_id = models.IntegerField(blank=True, null=True)       # starmerx_inventory_wms_report表ID
    product_id = models.IntegerField(blank=True, null=True)               # 产品ID
    product_tmpl_id = models.IntegerField(blank=True, null=True)          # product_template ID
    default_code = models.CharField(max_length=64, blank=True, null=True)            #  SKU
    name_template = models.CharField(max_length=128, blank=True, null=True)         #  产品名
    date = models.DateTimeField(blank=True, null=True)                   #  入库时间
    price_unit = models.FloatField(blank=True, null=True)                #  入库价格
    product_qty = models.FloatField(blank=True, null=True)                  #  入库数量
    origin = models.CharField(max_length=64, blank=True, null=True)          #  源单据
    picking_id = models.IntegerField(blank=True, null=True)                  #  入库主表ID
    state = models.CharField(max_length=20, blank=True, null=True)         #   状态
    warehouse_id = models.IntegerField(blank=True, null=True)         #  仓库ID
    warehouse_name = models.CharField(blank=True, null=True, max_length=128)    #  仓库名
    stock_qty = models.FloatField(blank=True, null=True)               #   所余库存


    class Meta:
        managed = False
        db_table = 'stock_move_wms_report'