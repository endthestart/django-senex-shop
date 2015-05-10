# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='from_email',
            field=models.EmailField(help_text='Email address to send e-mails with', max_length=254, verbose_name='from e-mail address'),
        ),
    ]
