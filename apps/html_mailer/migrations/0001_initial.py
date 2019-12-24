# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'html_mailer_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('from_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_text', self.gf('django.db.models.fields.TextField')()),
            ('message_html', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('when_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('priority', self.gf('django.db.models.fields.CharField')(default='2', max_length=1)),
        ))
        db.send_create_signal(u'html_mailer', ['Message'])

        # Adding model 'DontSendEntry'
        db.create_table(u'html_mailer_dontsendentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('when_added', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'html_mailer', ['DontSendEntry'])

        # Adding model 'MessageLog'
        db.create_table(u'html_mailer_messagelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('from_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message_text', self.gf('django.db.models.fields.TextField')()),
            ('message_html', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('when_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('priority', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('when_attempted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('log_message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'html_mailer', ['MessageLog'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'html_mailer_message')

        # Deleting model 'DontSendEntry'
        db.delete_table(u'html_mailer_dontsendentry')

        # Deleting model 'MessageLog'
        db.delete_table(u'html_mailer_messagelog')


    models = {
        u'html_mailer.dontsendentry': {
            'Meta': {'object_name': 'DontSendEntry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'when_added': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'html_mailer.message': {
            'Meta': {'object_name': 'Message'},
            'from_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_html': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'message_text': ('django.db.models.fields.TextField', [], {}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'2'", 'max_length': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'when_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'html_mailer.messagelog': {
            'Meta': {'object_name': 'MessageLog'},
            'from_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_message': ('django.db.models.fields.TextField', [], {}),
            'message_html': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'message_text': ('django.db.models.fields.TextField', [], {}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'to_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'when_added': ('django.db.models.fields.DateTimeField', [], {}),
            'when_attempted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['html_mailer']