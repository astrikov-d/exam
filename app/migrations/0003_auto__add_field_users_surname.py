# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Users.surname'
        db.add_column(u'app_users', 'surname',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Users.surname'
        db.delete_column(u'app_users', 'surname')


    models = {
        u'app.rooms': {
            'Meta': {'object_name': 'Rooms'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        u'app.users': {
            'Meta': {'object_name': 'Users'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['app']