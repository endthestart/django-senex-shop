# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug', unique_for_date=b'publish')),
                ('body', models.TextField(verbose_name='body')),
                ('tease', models.TextField(help_text='Concise text suggested. Does not appear in RSS feed.', verbose_name='tease', blank=True)),
                ('status', models.IntegerField(default=2, verbose_name='status', choices=[(1, 'Draft'), (2, 'Public')])),
                ('publish', models.DateTimeField(default=datetime.datetime.now, verbose_name='publish')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('photo', models.ImageField(upload_to=b'photos/%Y/%b/%d', blank=True)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('categories', models.ManyToManyField(related_name='posts', to='news.Category', blank=True)),
            ],
            options={
                'ordering': ('-publish',),
                'get_latest_by': 'publish',
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
            bases=(models.Model,),
        ),
    ]
