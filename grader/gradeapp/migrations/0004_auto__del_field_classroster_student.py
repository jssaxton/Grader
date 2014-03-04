# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ClassRoster.student'
        db.delete_column('gradeapp_classroster', 'student_id')

        # Adding M2M table for field student on 'ClassRoster'
        m2m_table_name = db.shorten_name('gradeapp_classroster_student')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classroster', models.ForeignKey(orm['gradeapp.classroster'], null=False)),
            ('user_info', models.ForeignKey(orm['gradeapp.user_info'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classroster_id', 'user_info_id'])


    def backwards(self, orm):
        # Adding field 'ClassRoster.student'
        db.add_column('gradeapp_classroster', 'student',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradeapp.user_info'], default=1),
                      keep_default=False)

        # Removing M2M table for field student on 'ClassRoster'
        db.delete_table(db.shorten_name('gradeapp_classroster_student'))


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
            'in_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gradeapp.MyClass']"}),
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