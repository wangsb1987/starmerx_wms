# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_auto_20170517_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('origin', models.CharField(blank=True, max_length=64, null=True)),
                ('date_due', models.DateField(blank=True, null=True)),
                ('check_total', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('reference', models.CharField(blank=True, max_length=64, null=True)),
                ('supplier_invoice_number', models.CharField(blank=True, max_length=64, null=True)),
                ('number', models.CharField(blank=True, max_length=64, null=True)),
                ('account_id', models.IntegerField(blank=True, null=True)),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('currency_id', models.IntegerField(blank=True, null=True)),
                ('partner_id', models.IntegerField(blank=True, null=True)),
                ('fiscal_position', models.IntegerField(blank=True, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('partner_bank_id', models.IntegerField(blank=True, null=True)),
                ('payment_term', models.IntegerField(blank=True, null=True)),
                ('reference_type', models.CharField(max_length=200)),
                ('journal_id', models.IntegerField(blank=True, null=True)),
                ('amount_tax', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('internal_number', models.CharField(blank=True, max_length=32, null=True)),
                ('reconciled', models.NullBooleanField()),
                ('residual', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('move_name', models.CharField(blank=True, max_length=64, null=True)),
                ('date_invoice', models.DateField(blank=True, null=True)),
                ('period_id', models.IntegerField(blank=True, null=True)),
                ('amount_untaxed', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('move_id', models.IntegerField(blank=True, null=True)),
                ('amount_total', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('sent', models.NullBooleanField()),
                ('section_id', models.IntegerField(blank=True, null=True)),
                ('payment_mode', models.IntegerField(blank=True, null=True)),
                ('stock_location', models.CharField(blank=True, max_length=200, null=True)),
                ('stock_warehouse', models.CharField(blank=True, max_length=200, null=True)),
                ('purchase_notes', models.TextField(blank=True, null=True)),
                ('discount_amount', models.FloatField(blank=True, null=True)),
                ('zfb_dealno', models.CharField(blank=True, max_length=50, null=True)),
                ('zfb_orderno', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'account_invoice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountInvoiceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('origin', models.CharField(blank=True, max_length=256, null=True)),
                ('uos_id', models.IntegerField(blank=True, null=True)),
                ('account_id', models.IntegerField(blank=True, null=True)),
                ('name', models.TextField()),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('invoice_id', models.IntegerField(blank=True, null=True)),
                ('price_unit', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('price_subtotal', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('account_analytic_id', models.IntegerField(blank=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=65535, max_digits=65535)),
                ('partner_id', models.IntegerField(blank=True, null=True)),
                ('product_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'account_invoice_line',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('journal', models.IntegerField()),
                ('partner_id', models.IntegerField(blank=True, null=True)),
                ('company_id', models.IntegerField()),
                ('bank_id', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'payment_mode',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('lang', models.CharField(blank=True, max_length=64, null=True)),
                ('company_id', models.IntegerField(blank=True, null=True)),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('ean13', models.CharField(blank=True, max_length=13, null=True)),
                ('color', models.IntegerField(blank=True, null=True)),
                ('image', models.BinaryField(blank=True, null=True)),
                ('use_parent_address', models.NullBooleanField()),
                ('active', models.NullBooleanField()),
                ('street', models.CharField(blank=True, max_length=128, null=True)),
                ('supplier', models.NullBooleanField()),
                ('city', models.CharField(blank=True, max_length=128, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('zip', models.CharField(blank=True, max_length=24, null=True)),
                ('title', models.IntegerField(blank=True, null=True)),
                ('function', models.CharField(blank=True, max_length=128, null=True)),
                ('country_id', models.IntegerField(blank=True, null=True)),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('employee', models.NullBooleanField()),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=240, null=True)),
                ('vat', models.CharField(blank=True, max_length=32, null=True)),
                ('website', models.CharField(blank=True, max_length=64, null=True)),
                ('fax', models.CharField(blank=True, max_length=64, null=True)),
                ('street2', models.CharField(blank=True, max_length=128, null=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('credit_limit', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('tz', models.CharField(blank=True, max_length=64, null=True)),
                ('customer', models.NullBooleanField()),
                ('image_medium', models.BinaryField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=64, null=True)),
                ('ref', models.CharField(blank=True, max_length=64, null=True)),
                ('image_small', models.BinaryField(blank=True, null=True)),
                ('birthdate', models.CharField(blank=True, max_length=64, null=True)),
                ('is_company', models.NullBooleanField()),
                ('state_id', models.IntegerField(blank=True, null=True)),
                ('notification_email_send', models.CharField(blank=True, max_length=256, null=True)),
                ('opt_out', models.NullBooleanField()),
                ('signup_type', models.CharField(blank=True, max_length=256, null=True)),
                ('signup_expiration', models.DateTimeField(blank=True, null=True)),
                ('signup_token', models.CharField(blank=True, max_length=256, null=True)),
                ('last_reconciliation_date', models.DateTimeField(blank=True, null=True)),
                ('debit_limit', models.FloatField(blank=True, null=True)),
                ('section_id', models.IntegerField(blank=True, null=True)),
                ('market_supplier', models.NullBooleanField()),
            ],
            options={
                'db_table': 'res_partner',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.NullBooleanField()),
                ('login', models.CharField(max_length=64)),
                ('password', models.CharField(blank=True, max_length=64, null=True)),
                ('company_id', models.IntegerField()),
                ('partner_id', models.IntegerField()),
                ('create_uid', models.IntegerField(blank=True, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('write_date', models.DateTimeField(blank=True, null=True)),
                ('write_uid', models.IntegerField(blank=True, null=True)),
                ('menu_id', models.IntegerField(blank=True, null=True)),
                ('login_date', models.DateField(blank=True, null=True)),
                ('signature', models.TextField(blank=True, null=True)),
                ('action_id', models.IntegerField(blank=True, null=True)),
                ('alias_id', models.IntegerField()),
                ('share', models.NullBooleanField()),
                ('default_section_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'res_users',
                'managed': False,
            },
        ),
    ]
