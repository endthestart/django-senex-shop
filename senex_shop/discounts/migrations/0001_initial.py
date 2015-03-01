# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senex_shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the discount.', max_length=255, verbose_name='name')),
                ('code', models.CharField(help_text='The code to use the discount.', max_length=30, verbose_name='code')),
                ('active', models.BooleanField(default=False, help_text='If the discount is active or not.', verbose_name='active')),
                ('type', models.CharField(default='Absolute', help_text='The type of discount.', max_length=128, verbose_name='type', choices=[('Absolute', 'Absolute - an absolute dollar amount'), ('Percentage', 'Percentage - a percentage of the total')])),
                ('value', models.DecimalField(decimal_places=2, max_digits=8, blank=True, help_text='The amount of the discount.', null=True, verbose_name='value')),
                ('products', models.ManyToManyField(related_name='discounts', verbose_name='products', to='senex_shop.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
