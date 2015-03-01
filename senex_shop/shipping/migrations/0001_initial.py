# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAndItemsCharges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.SlugField(unique=True, max_length=128, verbose_name='slug')),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('price_per_order', models.DecimalField(default=Decimal('0.00'), verbose_name='price per order', max_digits=12, decimal_places=2)),
                ('price_per_item', models.DecimalField(default=Decimal('0.00'), verbose_name='price per item', max_digits=12, decimal_places=2)),
                ('free_shipping_threshold', models.DecimalField(default=Decimal('0.00'), verbose_name='free shipping', max_digits=12, decimal_places=2)),
            ],
            options={
                'verbose_name': 'order and item charge',
                'verbose_name_plural': 'order and items charges',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeightBand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upper_limit', models.FloatField(help_text='The upper limit of this weight band.', verbose_name='upper limit')),
                ('charge', models.DecimalField(verbose_name='charge', max_digits=12, decimal_places=2)),
            ],
            options={
                'ordering': ['upper_limit'],
                'verbose_name': 'weight band',
                'verbose_name_plural': 'weight bands',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeightBased',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.SlugField(unique=True, max_length=128, verbose_name='slug')),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('upper_charge', models.DecimalField(help_text='This is the charge when the weight of the cart is greater than all the weight bands.', null=True, verbose_name='upper charge', max_digits=12, decimal_places=2)),
                ('default_weight', models.DecimalField(default=Decimal('0.00'), help_text='Default product weight when no weight attribute is defined.', verbose_name='default weight', max_digits=12, decimal_places=2)),
            ],
            options={
                'verbose_name': 'weight-based shipping method',
                'verbose_name_plural': 'weight-based shipping methods',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='weightband',
            name='method',
            field=models.ForeignKey(related_name='bands', verbose_name='method', to='shipping.WeightBased'),
            preserve_default=True,
        ),
    ]
