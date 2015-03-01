# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=255, null=True, verbose_name='full name', blank=True)),
                ('street1', models.CharField(help_text='The street 1 field.', max_length=80, verbose_name='street 1')),
                ('street2', models.CharField(help_text='APT/SUITE/OTHER', max_length=80, verbose_name='street 2', blank=True)),
                ('city', models.CharField(help_text='The city field.', max_length=50, verbose_name='city')),
                ('state', localflavor.us.models.USStateField(blank=True, help_text='The state field.', max_length=2, verbose_name='state', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('postal_code', models.CharField(help_text='The postal code field.', max_length=30, verbose_name='zip code')),
                ('country', models.CharField(default=b'United States', help_text='The country field.', max_length=100, verbose_name='country')),
            ],
            options={
                'verbose_name': 'billing address',
                'verbose_name_plural': 'billing addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=255, null=True, verbose_name='full name', blank=True)),
                ('street1', models.CharField(help_text='The street 1 field.', max_length=80, verbose_name='street 1')),
                ('street2', models.CharField(help_text='APT/SUITE/OTHER', max_length=80, verbose_name='street 2', blank=True)),
                ('city', models.CharField(help_text='The city field.', max_length=50, verbose_name='city')),
                ('state', localflavor.us.models.USStateField(blank=True, help_text='The state field.', max_length=2, verbose_name='state', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('postal_code', models.CharField(help_text='The postal code field.', max_length=30, verbose_name='zip code')),
                ('country', models.CharField(default=b'United States', help_text='The country field.', max_length=100, verbose_name='country')),
                ('phone_number', models.CharField(help_text='In case we need to call you about your order.', max_length=32, null=True, verbose_name='phone number', blank=True)),
                ('notes', models.TextField(help_text=b'Tell us anything we should know when delivering your order.', null=True, verbose_name='instructions', blank=True)),
            ],
            options={
                'verbose_name': 'shipping address',
                'verbose_name_plural': 'shipping addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('shippingaddress_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.ShippingAddress')),
                ('is_default_shipping', models.BooleanField(default=False, help_text='This is the default shipping address.', verbose_name='default shipping address')),
                ('is_default_billing', models.BooleanField(default=False, help_text='This is the default billing address.', verbose_name='default billing address')),
                ('num_orders', models.PositiveIntegerField(default=0, verbose_name='number of orders')),
                ('hash', models.CharField(verbose_name='address hash', max_length=255, editable=False, db_index=True)),
                ('user', models.ForeignKey(related_name='addresses', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-num_orders'],
                'verbose_name': 'user address',
                'verbose_name_plural': 'user addresses',
            },
            bases=('contact.shippingaddress',),
        ),
    ]
