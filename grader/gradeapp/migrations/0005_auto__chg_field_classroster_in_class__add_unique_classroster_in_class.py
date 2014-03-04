# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ClassRoster.in_class'
        db.alter_column('gradeapp_classroster', 'in_class_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gradeapp.MyClass'], unique=True))
        # Adding unique constraint on 'ClassRoster', fields ['in_class']
        db.create_unique('gradeapp_classroster', ['in_class_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ClassRoster', fields ['in_class']
        db.delete_unique('gradeapp_classroster', ['in_class_id'])


        # Changing field 'ClassRoster.in_class'
        db.alter_column('gradeapp_classroster', 'in_class_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.MyClass']))

    models = {
        'gradeapp.assignment_score': {
            'Meta': {'object_name': 'assignment_score'},
            'class_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.class_roster']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.class_roster': {
            'Meta': {'object_name': 'class_roster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.classroster': {
            'Meta': {'object_name': 'ClassRoster'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_class': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gradeapp.MyClass']", 'unique': 'True'}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gradeapp.user_info']", 'symmetrical': 'False'}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'ST'", 'max_length': '2'})
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
        'gradeapp.myclasslist': {
            'Meta': {'object_name': 'MyClassList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'myclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.MyClass']"})
        },
        'gradeapp.user_info': {
            'Meta': {'object_name': 'user_info'},
            'authenticate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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