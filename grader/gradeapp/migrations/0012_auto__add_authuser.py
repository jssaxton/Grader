# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AuthUser'
        db.create_table('gradeapp_authuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.user_info'])),
            ('class_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.MyClass'])),
            ('authorized', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gradeapp', ['AuthUser'])


    def backwards(self, orm):
        # Deleting model 'AuthUser'
        db.delete_table('gradeapp_authuser')


    models = {
        'gradeapp.assignment_score': {
            'Meta': {'object_name': 'assignment_score'},
            'class_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.class_roster']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.authuser': {
            'Meta': {'object_name': 'AuthUser'},
            'authorized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'class_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.MyClass']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.class_roster': {
            'Meta': {'object_name': 'class_roster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.classroster': {
            'Meta': {'object_name': 'ClassRoster'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'class_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_class': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['gradeapp.MyClass']"}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.myclass': {
            'Meta': {'object_name': 'MyClass'},
            'authenticate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'class_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'teacher': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'gradeapp.user_info': {
            'Meta': {'object_name': 'user_info'},
            'authenticate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'class_list': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gradeapp.MyClass']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_class_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'init_class_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'init_class_semester': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'ST'", 'max_length': '2'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['gradeapp']