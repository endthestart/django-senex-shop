# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150510_1101'),
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_per_order', models.DecimalField(default=Decimal('0.00'), verbose_name='price per order', max_digits=12, decimal_places=2)),
                ('price_per_item', models.DecimalField(default=Decimal('0.00'), verbose_name='price per item', max_digits=12, decimal_places=2)),
                ('free_shipping_threshold', models.DecimalField(null=True, verbose_name='free shipping threshold', max_digits=12, decimal_places=2, blank=True)),
                ('shop', models.OneToOneField(related_name='shipping_module', to='core.Shop')),
            ],
            options={
                'verbose_name': 'shipping module',
                'verbose_name_plural': 'shipping modules',
            },
        ),
        migrations.DeleteModel(
            name='OrderAndItemsCharges',
        ),
        migrations.RemoveField(
            model_name='weightband',
            name='method',
        ),
        migrations.DeleteModel(
            name='WeightBand',
        ),
        migrations.DeleteModel(
            name='WeightBased',
        ),
    ]
