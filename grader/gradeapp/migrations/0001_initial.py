# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'user_info'
        db.create_table('gradeapp_user_info', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user_type', self.gf('django.db.models.fields.CharField')(default='ST', max_length=2)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('authenticate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('init_class_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('init_class_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('init_class_semester', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('gradeapp', ['user_info'])

        # Adding model 'ClassRoster'
        db.create_table('gradeapp_classroster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.user_info'])),
        ))
        db.send_create_signal('gradeapp', ['ClassRoster'])

        # Adding model 'MyClass'
        db.create_table('gradeapp_myclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('class_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('teacher', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('semester', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('class_roster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.ClassRoster'])),
            ('authenticate', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gradeapp', ['MyClass'])

        # Adding model 'MyClassList'
        db.create_table('gradeapp_myclasslist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('myclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.MyClass'])),
        ))
        db.send_create_signal('gradeapp', ['MyClassList'])

        # Adding model 'class_roster'
        db.create_table('gradeapp_class_roster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.user_info'])),
        ))
        db.send_create_signal('gradeapp', ['class_roster'])

        # Adding model 'assignment_score'
        db.create_table('gradeapp_assignment_score', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.user_info'])),
            ('class_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.class_roster'])),
        ))
        db.send_create_signal('gradeapp', ['assignment_score'])


    def backwards(self, orm):
        # Deleting model 'user_info'
        db.delete_table('gradeapp_user_info')

        # Deleting model 'ClassRoster'
        db.delete_table('gradeapp_classroster')

        # Deleting model 'MyClass'
        db.delete_table('gradeapp_myclass')

        # Deleting model 'MyClassList'
        db.delete_table('gradeapp_myclasslist')

        # Deleting model 'class_roster'
        db.delete_table('gradeapp_class_roster')

        # Deleting model 'assignment_score'
        db.delete_table('gradeapp_assignment_score')


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
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.myclass': {
            'Meta': {'object_name': 'MyClass'},
            'authenticate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'class_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'class_roster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.ClassRoster']"}),
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