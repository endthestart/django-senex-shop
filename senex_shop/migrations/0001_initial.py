# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'senex_shop_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='child', null=True, to=orm['senex_shop.Category'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'senex_shop', ['Category'])

        # Adding M2M table for field related_categories on 'Category'
        m2m_table_name = db.shorten_name(u'senex_shop_category_related_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_category', models.ForeignKey(orm[u'senex_shop.category'], null=False)),
            ('to_category', models.ForeignKey(orm[u'senex_shop.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_category_id', 'to_category_id'])

        # Adding model 'Product'
        db.create_table(u'senex_shop_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'category', to=orm['senex_shop.Category'])),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('stock', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=18, decimal_places=6)),
            ('short_description', self.gf('django.db.models.fields.TextField')(default='', max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'senex_shop', ['Product'])

        # Adding model 'ProductImage'
        db.create_table(u'senex_shop_productimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['senex_shop.Product'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'senex_shop', ['ProductImage'])

        # Adding unique constraint on 'ProductImage', fields ['product', 'sort']
        db.create_unique(u'senex_shop_productimage', ['product_id', 'sort'])

        # Adding model 'OptionGroup'
        db.create_table(u'senex_shop_optiongroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'senex_shop', ['OptionGroup'])

        # Adding model 'Option'
        db.create_table(u'senex_shop_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['senex_shop.OptionGroup'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('price_change', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=8, decimal_places=2)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'senex_shop', ['Option'])

        # Adding unique constraint on 'Option', fields ['option_group', 'value']
        db.create_unique(u'senex_shop_option', ['option_group_id', 'value'])

        # Adding model 'AttributeOption'
        db.create_table(u'senex_shop_attributeoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('validation', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('error_message', self.gf('django.db.models.fields.CharField')(default=u'invalid entry', max_length=100)),
        ))
        db.send_create_signal(u'senex_shop', ['AttributeOption'])

        # Adding model 'ProductAttribute'
        db.create_table(u'senex_shop_productattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['senex_shop.Product'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['senex_shop.AttributeOption'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'senex_shop', ['ProductAttribute'])


    def backwards(self, orm):
        # Removing unique constraint on 'Option', fields ['option_group', 'value']
        db.delete_unique(u'senex_shop_option', ['option_group_id', 'value'])

        # Removing unique constraint on 'ProductImage', fields ['product', 'sort']
        db.delete_unique(u'senex_shop_productimage', ['product_id', 'sort'])

        # Deleting model 'Category'
        db.delete_table(u'senex_shop_category')

        # Removing M2M table for field related_categories on 'Category'
        db.delete_table(db.shorten_name(u'senex_shop_category_related_categories'))

        # Deleting model 'Product'
        db.delete_table(u'senex_shop_product')

        # Deleting model 'ProductImage'
        db.delete_table(u'senex_shop_productimage')

        # Deleting model 'OptionGroup'
        db.delete_table(u'senex_shop_optiongroup')

        # Deleting model 'Option'
        db.delete_table(u'senex_shop_option')

        # Deleting model 'AttributeOption'
        db.delete_table(u'senex_shop_attributeoption')

        # Deleting model 'ProductAttribute'
        db.delete_table(u'senex_shop_productattribute')


    models = {
        u'senex_shop.attributeoption': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'AttributeOption'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'error_message': ('django.db.models.fields.CharField', [], {'default': "u'invalid entry'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'validation': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'senex_shop.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child'", 'null': 'True', 'to': u"orm['senex_shop.Category']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'related_categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_categories_rel_+'", 'null': 'True', 'to': u"orm['senex_shop.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'senex_shop.option': {
            'Meta': {'ordering': "('option_group', 'ordering')", 'unique_together': "(('option_group', 'value'),)", 'object_name': 'Option'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['senex_shop.OptionGroup']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price_change': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '8', 'decimal_places': '2'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'senex_shop.optiongroup': {
            'Meta': {'ordering': "('ordering',)", 'object_name': 'OptionGroup'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'senex_shop.product': {
            'Meta': {'ordering': "('ordering', 'name')", 'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'category'", 'to': u"orm['senex_shop.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'stock': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '6'})
        },
        u'senex_shop.productattribute': {
            'Meta': {'ordering': "('option__sort_order',)", 'object_name': 'ProductAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['senex_shop.AttributeOption']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['senex_shop.Product']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'senex_shop.productimage': {
            'Meta': {'ordering': "['sort']", 'unique_together': "(('product', 'sort'),)", 'object_name': 'ProductImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['senex_shop.Product']"}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['senex_shop']