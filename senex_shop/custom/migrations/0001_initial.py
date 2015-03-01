# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senex_shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomProduct',
            fields=[
                ('product', models.OneToOneField(primary_key=True, serialize=False, to='senex_shop.Product', verbose_name='Product')),
                ('option_group', models.ManyToManyField(to='senex_shop.OptionGroup', verbose_name='option group', blank=True)),
            ],
            options={
                'verbose_name': 'Custom Product',
                'verbose_name_plural': 'Custom Products',
            },
            bases=(models.Model,),
        ),
    ]
