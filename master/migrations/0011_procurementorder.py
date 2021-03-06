# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-22 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0010_starmerxinventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcurementOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('product_uom', models.IntegerField(blank=True, null=True)),
                ('product_uos_qty', models.FloatField(blank=True, null=True)),
                ('procure_method', models.CharField(blank=True, max_length=15, null=True)),
                ('product_qty', models.FloatField(blank=True, null=True)),
                ('product_uos', models.IntegerField(blank=True, null=True)),
                ('message', models.CharField(blank=True, max_length=124, null=True)),
                ('location_id', models.IntegerField(blank=True, null=True)),
                ('move_id', models.IntegerField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('date_planned', models.DateTimeField(blank=True, null=True)),
                ('close_move', models.NullBooleanField()),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('date_close', models.DateTimeField(blank=True, null=True)),
                ('priority', models.CharField(blank=True, max_length=15, null=True)),
                ('state', models.CharField(blank=True, max_length=15, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('purchase_id', models.IntegerField(blank=True, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('origin', models.CharField(blank=True, max_length=128, null=True)),
                ('sale_id', models.IntegerField(blank=True, null=True)),
                ('is_declare', models.CharField(blank=True, max_length=15, null=True)),
                ('procurement_order_id', models.IntegerField(blank=True, null=True)),
                ('stock_state', models.CharField(blank=True, max_length=15, null=True)),
                ('stockin_qty', models.IntegerField(blank=True, null=True)),
                ('stockin_date_group', models.CharField(blank=True, max_length=64, null=True)),
                ('stockin_date', models.DateTimeField(blank=True, null=True)),
                ('account_id', models.CharField(blank=True, max_length=64, null=True)),
                ('asin', models.CharField(blank=True, max_length=128, null=True)),
                ('is_first', models.CharField(blank=True, max_length=15, null=True)),
                ('virtual_stockin_qty', models.IntegerField(blank=True, null=True)),
                ('confirm_move_qty', models.IntegerField(blank=True, null=True)),
                ('move_state', models.CharField(blank=True, max_length=15, null=True)),
                ('confirm_move_qty_total', models.IntegerField(blank=True, null=True)),
                ('this_confirm_qty', models.IntegerField(blank=True, null=True)),
                ('this_confirm_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'procurement_order',
                'managed': False,
            },
        ),
    ]
