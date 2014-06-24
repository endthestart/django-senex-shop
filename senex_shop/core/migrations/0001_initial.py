# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shop'
        db.create_table(u'core_shop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('shop_owner', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(default='<name>', max_length=80, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Shop'])


    def backwards(self, orm):
        # Deleting model 'Shop'
        db.delete_table(u'core_shop')


    models = {
        u'core.shop': {
            'Meta': {'object_name': 'Shop'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'default': "'<name>'", 'max_length': '80', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'shop_owner': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['core']