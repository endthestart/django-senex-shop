# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=128, verbose_name='order number', db_index=True)),
                ('total_incl_tax', models.DecimalField(verbose_name='order total (inc. tax)', max_digits=12, decimal_places=2)),
                ('total_excl_tax', models.DecimalField(verbose_name='order total (excl tax)', max_digits=12, decimal_places=2)),
                ('shipping_incl_tax', models.DecimalField(verbose_name='shipping charge (inc. tax)', max_digits=12, decimal_places=2)),
                ('shipping_excl_tax', models.DecimalField(verbose_name='shipping charge (excl. tax)', max_digits=12, decimal_places=2)),
                ('shipping_method', models.CharField(max_length=128, null=True, verbose_name='shipping method', blank=True)),
                ('shipping_code', models.CharField(default=b'', max_length=128, blank=True)),
                ('status', models.CharField(max_length=100, null=True, verbose_name='status', blank=True)),
                ('guest_email', models.EmailField(max_length=75, null=True, verbose_name='guest email address', blank=True)),
                ('date_ordered', models.DateField(auto_now_add=True, db_index=True)),
                ('billing_address', models.ForeignKey(verbose_name='billing address', blank=True, to='contact.BillingAddress', null=True)),
                ('cart', models.ForeignKey(blank=True, to='cart.Cart', null=True)),
            ],
            options={
                'ordering': ('user',),
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(verbose_name='amount of transaction', max_digits=12, decimal_places=2)),
                ('order', models.ForeignKey(to='checkout.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='payment name')),
                ('code', models.SlugField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StripeCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge_id', models.CharField(max_length=32)),
                ('card_brand', models.CharField(max_length=32)),
                ('last4', models.CharField(max_length=4)),
            ],
            options={
                'ordering': ('charge_id',),
                'verbose_name': 'stripe charge',
                'verbose_name_plural': 'stripe charges',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPaymentDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stripe_id', models.CharField(max_length=128, null=True, verbose_name='stripe id', blank=True)),
                ('user', models.ForeignKey(verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('user',),
                'verbose_name': 'User Payment Details',
                'verbose_name_plural': 'User Payment Details',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paymentdetails',
            name='payment_type',
            field=models.ForeignKey(to='checkout.PaymentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='charge',
            field=models.ForeignKey(verbose_name='charge', blank=True, to='checkout.StripeCharge', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(verbose_name='shipping address', blank=True, to='contact.ShippingAddress', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
