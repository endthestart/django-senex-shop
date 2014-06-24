# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sale'
        db.create_table(u'checkout_sale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('charge_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'checkout', ['Sale'])

        # Adding model 'Order'
        db.create_table(u'checkout_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cart.Cart'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['custom_auth.User'], null=True, blank=True)),
            ('billing_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.BillingAddress'], null=True, blank=True)),
            ('total_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('total_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_incl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_excl_tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('shipping_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.ShippingAddress'], null=True, blank=True)),
            ('shipping_method', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('shipping_code', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('guest_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('date_ordered', self.gf('django.db.models.fields.DateField')(auto_now_add=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'checkout', ['Order'])

        # Adding model 'PaymentType'
        db.create_table(u'checkout_paymenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=128)),
        ))
        db.send_create_signal(u'checkout', ['PaymentType'])

        # Adding model 'PaymentDetails'
        db.create_table(u'checkout_paymentdetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkout.Order'])),
            ('payment_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkout.PaymentType'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'checkout', ['PaymentDetails'])

        # Adding model 'UserPaymentDetails'
        db.create_table(u'checkout_userpaymentdetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['custom_auth.User'], null=True, blank=True)),
            ('stripe_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'checkout', ['UserPaymentDetails'])


    def backwards(self, orm):
        # Deleting model 'Sale'
        db.delete_table(u'checkout_sale')

        # Deleting model 'Order'
        db.delete_table(u'checkout_order')

        # Deleting model 'PaymentType'
        db.delete_table(u'checkout_paymenttype')

        # Deleting model 'PaymentDetails'
        db.delete_table(u'checkout_paymentdetails')

        # Deleting model 'UserPaymentDetails'
        db.delete_table(u'checkout_userpaymentdetails')


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
        u'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['custom_auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'checkout.order': {
            'Meta': {'ordering': "('user',)", 'object_name': 'Order'},
            'billing_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.BillingAddress']", 'null': 'True', 'blank': 'True'}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cart.Cart']", 'null': 'True', 'blank': 'True'}),
            'date_ordered': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'guest_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.ShippingAddress']", 'null': 'True', 'blank': 'True'}),
            'shipping_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'shipping_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'shipping_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'shipping_method': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'total_excl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'total_incl_tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['custom_auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'checkout.paymentdetails': {
            'Meta': {'object_name': 'PaymentDetails'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkout.Order']"}),
            'payment_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkout.PaymentType']"})
        },
        u'checkout.paymenttype': {
            'Meta': {'object_name': 'PaymentType'},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'checkout.sale': {
            'Meta': {'object_name': 'Sale'},
            'charge_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'checkout.userpaymentdetails': {
            'Meta': {'ordering': "('user',)", 'object_name': 'UserPaymentDetails'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['custom_auth.User']", 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['checkout']