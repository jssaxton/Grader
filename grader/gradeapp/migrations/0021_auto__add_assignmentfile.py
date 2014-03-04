# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AssignmentFile'
        db.create_table('gradeapp_assignmentfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.Assignment'])),
            ('my_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_comment', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),
            ('date_uploaded', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('gradeapp', ['AssignmentFile'])


    def backwards(self, orm):
        # Deleting model 'AssignmentFile'
        db.delete_table('gradeapp_assignmentfile')


    models = {
        'gradeapp.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'already_graded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'already_uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assign_date': ('django.db.models.fields.DateField', [], {}),
            'assignment_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'real_score': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'retry_limit': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'default': '0'}),
            'to_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.MyClass']"}),
            'to_student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.assignment_score': {
            'Meta': {'object_name': 'assignment_score'},
            'class_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.class_roster']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"})
        },
        'gradeapp.assignmentfile': {
            'Meta': {'object_name': 'AssignmentFile'},
            'date_uploaded': ('django.db.models.fields.DateField', [], {}),
            'file_comment': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'to_assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.Assignment']"})
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
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gradeapp.user_info']"}),
            'teacher': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
        'gradeapp.myinbox': {
            'Meta': {'object_name': 'MyInbox'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'received_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"}),
            'sent_by': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'gradeapp.myoutbox': {
            'Meta': {'object_name': 'MyOutbox'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'received_by': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sent_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.user_info']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'ST'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['gradeapp']