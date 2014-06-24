# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShippingAddress'
        db.create_table(u'contact_shippingaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('street1', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('street2', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django.db.models.fields.CharField')(default='United States', max_length=100)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'contact', ['ShippingAddress'])

        # Adding model 'UserAddress'
        db.create_table(u'contact_useraddress', (
            (u'shippingaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contact.ShippingAddress'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='addresses', to=orm['custom_auth.User'])),
            ('is_default_shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_default_billing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_orders', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'contact', ['UserAddress'])

        # Adding model 'BillingAddress'
        db.create_table(u'contact_billingaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('street1', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('street2', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('country', self.gf('django.db.models.fields.CharField')(default='United States', max_length=100)),
        ))
        db.send_create_signal(u'contact', ['BillingAddress'])


    def backwards(self, orm):
        # Deleting model 'ShippingAddress'
        db.delete_table(u'contact_shippingaddress')

        # Deleting model 'UserAddress'
        db.delete_table(u'contact_useraddress')

        # Deleting model 'BillingAddress'
        db.delete_table(u'contact_billingaddress')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contact.billingaddress': {
            'Meta': {'object_name': 'BillingAddress'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'United States'", 'max_length': '100'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2', 'blank': 'True'}),
            'street1': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'street2': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        u'contact.shippingaddress': {
            'Meta': {'object_name': 'ShippingAddress'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'United States'", 'max_length': '100'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2', 'blank': 'True'}),
            'street1': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'street2': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        u'contact.useraddress': {
            'Meta': {'ordering': "['-num_orders']", 'object_name': 'UserAddress', '_ormbases': [u'contact.ShippingAddress']},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'is_default_billing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_default_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_orders': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'shippingaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['contact.ShippingAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': u"orm['custom_auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'custom_auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['contact']