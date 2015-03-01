# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomProduct'
        db.create_table(u'custom_customproduct', (
            ('product', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['senex_shop.Product'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'custom', ['CustomProduct'])

        # Adding M2M table for field option_group on 'CustomProduct'
        m2m_table_name = db.shorten_name(u'custom_customproduct_option_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customproduct', models.ForeignKey(orm[u'custom.customproduct'], null=False)),
            ('optiongroup', models.ForeignKey(orm[u'senex_shop.optiongroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customproduct_id', 'optiongroup_id'])


    def backwards(self, orm):
        # Deleting model 'CustomProduct'
        db.delete_table(u'custom_customproduct')

        # Removing M2M table for field option_group on 'CustomProduct'
        db.delete_table(db.shorten_name(u'custom_customproduct_option_group'))


    models = {
        u'custom.customproduct': {
            'Meta': {'object_name': 'CustomProduct'},
            'option_group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['senex_shop.OptionGroup']", 'symmetrical': 'False', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['senex_shop.Product']", 'unique': 'True', 'primary_key': 'True'})
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
        }
    }

    complete_apps = ['custom']