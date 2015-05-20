# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150510_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='map_url',
            field=models.TextField(help_text='An embedded map url to include on the contact page.', verbose_name='map url', blank=True),
        ),
    ]
