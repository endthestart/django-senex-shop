# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('senex_shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Open', help_text='The status of the cart', max_length=128, verbose_name='status', choices=[(b'Open', 'Open - currently active'), (b'Merged', 'Merged - joined to another cart'), (b'Saved', 'Saved - for items to be purchased later'), (b'Frozen', 'Frozen - the cart cannot be modified'), (b'Submitted', 'Submitted - has been ordered at the checkout')])),
                ('description', models.CharField(max_length=10, null=True, verbose_name='description', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('date_submitted', models.DateTimeField(help_text='The date the cart was submitted.', null=True, verbose_name='date submitted', blank=True)),
                ('discount', models.ForeignKey(verbose_name='discount', blank=True, to='discounts.Discount', null=True)),
                ('user', models.ForeignKey(verbose_name='customer', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Shopping Cart',
                'verbose_name_plural': 'Shopping Carts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('cart', models.ForeignKey(verbose_name='cart', to='cart.Cart')),
                ('product', models.ForeignKey(verbose_name='product', to='senex_shop.Product')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartItemDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(verbose_name='detail')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('price_change', models.DecimalField(decimal_places=2, max_digits=8, blank=True, help_text='The cost change of the detail.', null=True, verbose_name='price change')),
                ('sort_order', models.IntegerField(help_text='The display order for this group.', verbose_name='sort order')),
                ('cartitem', models.ForeignKey(related_name='details', to='cart.CartItem')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Cart Item Detail',
                'verbose_name_plural': 'Cart Item Details',
            },
            bases=(models.Model,),
        ),
    ]
