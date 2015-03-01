# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, verbose_name='description')),
                ('name', models.SlugField(max_length=100, verbose_name='name')),
                ('validation', models.CharField(max_length=100, verbose_name='validation', choices=[(b'product.utils.validation_simple', 'One or more characters'), (b'product.utils.validation_integer', 'Integer number'), (b'product.utils.validation_yesno', 'Yes or No'), (b'product.utils.validation_decimal', 'Decimal number')])),
                ('sort_order', models.IntegerField(default=1, verbose_name='sort order')),
                ('error_message', models.CharField(default='invalid entry', max_length=100, verbose_name='error message')),
            ],
            options={
                'ordering': ('sort_order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(help_text='Used for URLs, auto-generated from name if blank', verbose_name='slug', blank=True)),
                ('path', models.CharField(help_text='The path of the category for use in URLs', max_length=255, null=True, verbose_name='path', blank=True)),
                ('name_path', models.CharField(help_text='The path of the category for use in text', max_length=255, null=True, verbose_name='name path', blank=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(help_text='The category image used for display.', upload_to=b'category', null=True, verbose_name='image', blank=True)),
                ('meta', models.TextField(help_text='Meta description for this category.', null=True, verbose_name='meta description', blank=True)),
                ('description', models.TextField(help_text='Description of the category.', verbose_name='description', blank=True)),
                ('ordering', models.IntegerField(default=0, help_text='Override alphabetical order in the category display.', verbose_name='ordering')),
                ('is_active', models.BooleanField(default=True, help_text='Whether or not the category is active.', verbose_name='active')),
                ('parent', models.ForeignKey(related_name='child', blank=True, to='senex_shop.Category', null=True)),
                ('related_categories', models.ManyToManyField(related_name='related_categories_rel_+', null=True, verbose_name='related categories', to='senex_shop.Category', blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The displayed value of the option.', max_length=50, verbose_name='name')),
                ('value', models.CharField(help_text='The stored value of the option.', max_length=50, verbose_name='value')),
                ('price_change', models.DecimalField(default=0.0, help_text='The change in cost for a product.', verbose_name='price change', max_digits=8, decimal_places=2)),
                ('ordering', models.IntegerField(default=0, help_text='Override alphabetical order in the category display.', verbose_name='ordering')),
            ],
            options={
                'ordering': ('option_group', 'ordering'),
                'verbose_name': 'option',
                'verbose_name_plural': 'options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the option group.', max_length=50, verbose_name='name')),
                ('display', models.CharField(default=b'', help_text='The display name of the option group.', max_length=50, verbose_name='display', blank=True)),
                ('description', models.TextField(help_text='This should be a more lengthy description of the option group.', null=True, verbose_name='description', blank=True)),
                ('ordering', models.IntegerField(default=0, help_text='Override alphabetical order in the category display.', verbose_name='ordering')),
            ],
            options={
                'ordering': ('ordering',),
                'verbose_name': 'option group',
                'verbose_name_plural': 'option groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the product.', max_length=255, null=True, verbose_name='name', blank=True)),
                ('slug', models.SlugField(help_text='Used for URLs, auto-generated from name if blank.', max_length=255, verbose_name='slug', blank=True)),
                ('sku', models.CharField(help_text='Defaults to slug if left blank.', max_length=255, null=True, verbose_name='sku', blank=True)),
                ('created', models.DateTimeField(help_text='The date and time the item was created.', verbose_name='date created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text='The date and time the item was modified.', verbose_name='date modified', auto_now=True)),
                ('ordering', models.IntegerField(default=0, help_text='Override default alphabetical ordering', verbose_name='ordering')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, blank=True, help_text='The cost of the item.', null=True, verbose_name='price')),
                ('stock', models.IntegerField(default=b'0', verbose_name='stock')),
                ('short_description', models.TextField(default=b'', help_text='This should be a 1 or 2 line description of the product.', max_length=200, verbose_name='short description of the product.', blank=True)),
                ('description', models.TextField(help_text='This should be a more lengthy description of the product.', null=True, verbose_name='description', blank=True)),
                ('meta', models.TextField(help_text='The meta description of the product.', max_length=200, null=True, verbose_name='meta description', blank=True)),
                ('active', models.BooleanField(default=True, help_text='Denotes if the product is available or not.', verbose_name='active')),
                ('category', models.ForeignKey(related_name='category', to='senex_shop.Category')),
            ],
            options={
                'ordering': ('ordering', 'name'),
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, verbose_name='value')),
                ('option', models.ForeignKey(to='senex_shop.AttributeOption')),
                ('product', models.ForeignKey(to='senex_shop.Product')),
            ],
            options={
                'ordering': ('option__sort_order',),
                'verbose_name': 'Product Attribute',
                'verbose_name_plural': 'Product Attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(help_text='The product image used for display.', upload_to=b'product', null=True, verbose_name='image', blank=True)),
                ('sort', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('product', models.ForeignKey(to='senex_shop.Product')),
            ],
            options={
                'ordering': ['sort'],
                'verbose_name': 'product image',
                'verbose_name_plural': 'product images',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='productimage',
            unique_together=set([('product', 'sort')]),
        ),
        migrations.AddField(
            model_name='option',
            name='option_group',
            field=models.ForeignKey(to='senex_shop.OptionGroup'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='option',
            unique_together=set([('option_group', 'value')]),
        ),
    ]
