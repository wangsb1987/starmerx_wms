# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_rescurrency'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('ean13', models.CharField(blank=True, max_length=13, null=True)),
                ('color', models.IntegerField(blank=True, null=True)),
                ('image', models.BinaryField(blank=True, null=True)),
                ('price_extra', models.FloatField(blank=True, null=True)),
                ('default_code', models.CharField(blank=True, max_length=64, null=True)),
                ('name_template', models.CharField(blank=True, max_length=128, null=True)),
                ('active', models.NullBooleanField()),
                ('variants', models.CharField(blank=True, max_length=128, null=True)),
                ('image_medium', models.BinaryField(blank=True, null=True)),
                ('image_small', models.BinaryField(blank=True, null=True)),
                ('product_tmpl_id', models.IntegerField(blank=True, null=True)),
                ('price_margin', models.FloatField(blank=True, null=True)),
                ('track_outgoing', models.NullBooleanField()),
                ('track_incoming', models.NullBooleanField()),
                ('valuation', models.CharField(blank=True, max_length=128, null=True)),
                ('track_production', models.NullBooleanField()),
                ('english_name', models.CharField(blank=True, max_length=128, null=True)),
                ('hr_expense_ok', models.NullBooleanField()),
                ('us_pack_id', models.IntegerField(blank=True, null=True)),
                ('pack_id', models.IntegerField(blank=True, null=True)),
                ('starmerx_price', models.FloatField(blank=True, null=True)),
                ('last_week_sale_data', models.FloatField(blank=True, null=True)),
                ('last_purchase_price', models.FloatField(blank=True, null=True)),
                ('gz_pack_id', models.IntegerField(blank=True, null=True)),
                ('last_mounth_sale_data', models.FloatField(blank=True, null=True)),
                ('last_2week_sale_data', models.FloatField(blank=True, null=True)),
                ('vip_pack_id', models.IntegerField(blank=True, null=True)),
                ('sea_pack_id', models.IntegerField(blank=True, null=True)),
                ('real_pack_id', models.IntegerField(blank=True, null=True)),
                ('last_purchaser', models.IntegerField(blank=True, null=True)),
                ('gvip_pack_id', models.IntegerField(blank=True, null=True)),
                ('cvip_pack_id', models.IntegerField(blank=True, null=True)),
                ('csea_pack_id', models.IntegerField(blank=True, null=True)),
                ('chfc_pack_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'product_product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResProductTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('warranty', models.FloatField(blank=True, null=True)),
                ('uos_id', models.IntegerField(blank=True, null=True)),
                ('list_price', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('weight_net', models.FloatField(blank=True, null=True)),
                ('standard_price', models.FloatField(blank=True, null=True)),
                ('mes_type', models.CharField(blank=True, max_length=128, null=True)),
                ('uom_id', models.IntegerField(blank=True, null=True)),
                ('description_purchase', models.TextField(blank=True, null=True)),
                ('cost_method', models.CharField(blank=True, max_length=128, null=True)),
                ('categ_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('uos_coeff', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('sale_ok', models.NullBooleanField()),
                ('description_sale', models.TextField(blank=True, null=True)),
                ('product_manager', models.IntegerField(blank=True, null=True)),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('produce_delay', models.FloatField(blank=True, null=True)),
                ('uom_po_id', models.IntegerField(blank=True, null=True)),
                ('rental', models.NullBooleanField()),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('loc_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_row', models.CharField(blank=True, max_length=16, null=True)),
                ('sale_delay', models.FloatField(blank=True, null=True)),
                ('loc_case', models.CharField(blank=True, max_length=16, null=True)),
                ('supply_method', models.CharField(blank=True, max_length=128, null=True)),
                ('procure_method', models.CharField(blank=True, max_length=128, null=True)),
                ('purchase_ok', models.NullBooleanField()),
                ('loc_us_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_us_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_gz_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_gz_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_vip_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_sea_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_vip_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_sea_row', models.CharField(blank=True, max_length=16, null=True)),
                ('his_row', models.CharField(blank=True, max_length=16, null=True)),
                ('his_gz_row', models.CharField(blank=True, max_length=16, null=True)),
                ('his_sea_row', models.CharField(blank=True, max_length=16, null=True)),
                ('his_gz_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_us_row', models.CharField(blank=True, max_length=16, null=True)),
                ('his_vip_row', models.CharField(blank=True, max_length=16, null=True)),
                ('his_vip_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_us_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_sea_rack', models.IntegerField(blank=True, null=True)),
                ('pro_liquid_type', models.IntegerField(blank=True, null=True)),
                ('battery_type', models.IntegerField(blank=True, null=True)),
                ('pro_battery_type', models.IntegerField(blank=True, null=True)),
                ('liquid_type', models.IntegerField(blank=True, null=True)),
                ('loc_csea_row', models.CharField(blank=True, max_length=16, null=True)),
                ('his_gvip_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_csea_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_gvip_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_gvip_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_gvip_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_csea_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_csea_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_cvip_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_cvip_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_cvip_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('his_cvip_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_chfc_row', models.CharField(blank=True, max_length=16, null=True)),
                ('loc_chfc_rack', models.CharField(blank=True, max_length=16, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('width', models.FloatField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'product_template',
                'managed': False,
            },
        ),
    ]
