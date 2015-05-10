# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senex_shop', '0002_auto_20150510_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='height',
            field=models.FloatField(default=0.0, verbose_name='height'),
        ),
        migrations.AddField(
            model_name='product',
            name='length',
            field=models.FloatField(default=0.0, verbose_name='length'),
        ),
        migrations.AddField(
            model_name='product',
            name='shipping_required',
            field=models.BooleanField(default=True, verbose_name='shipping required'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.FloatField(default=0.0, verbose_name='weight'),
        ),
        migrations.AddField(
            model_name='product',
            name='width',
            field=models.FloatField(default=0.0, verbose_name='width'),
        ),
    ]
