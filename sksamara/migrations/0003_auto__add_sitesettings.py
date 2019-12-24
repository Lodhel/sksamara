# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteSettings'
        db.create_table(u'sksamara_sitesettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipients', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'sksamara', ['SiteSettings'])


    def backwards(self, orm):
        # Deleting model 'SiteSettings'
        db.delete_table(u'sksamara_sitesettings')


    models = {
        u'sksamara.connectionrequest': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'ConnectionRequest'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {})
        },
        u'sksamara.connectionrequestfile': {
            'Meta': {'object_name': 'ConnectionRequestFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sksamara.ConnectionRequest']"})
        },
        u'sksamara.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipients': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'sksamara.staticpage': {
            'Meta': {'ordering': "('order',)", 'object_name': 'StaticPage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'text': ('tinymce.models.HTMLField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['sksamara']