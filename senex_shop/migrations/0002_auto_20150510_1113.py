# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senex_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='related_categories',
            field=models.ManyToManyField(related_name='related_categories_rel_+', verbose_name='related categories', to='senex_shop.Category', blank=True),
        ),
    ]
