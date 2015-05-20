# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senex_shop', '0003_auto_20150510_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shipping_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, blank=True, help_text='The fixed shiping cost of the item.', null=True, verbose_name='shipping price'),
        ),
    ]
