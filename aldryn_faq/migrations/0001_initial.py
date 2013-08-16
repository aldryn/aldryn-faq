# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryTranslation'
        db.create_table(u'aldryn_faq_category_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['aldryn_faq.Category'])),
        ))
        db.send_create_signal(u'aldryn_faq', ['CategoryTranslation'])

        # Adding unique constraint on 'CategoryTranslation', fields ['language_code', 'master']
        db.create_unique(u'aldryn_faq_category_translation', ['language_code', 'master_id'])

        # Adding model 'Category'
        db.create_table(u'aldryn_faq_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'aldryn_faq', ['Category'])

        # Adding model 'Question'
        db.create_table(u'aldryn_faq_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('category', self.gf('adminsortable.fields.SortableForeignKey')(to=orm['aldryn_faq.Category'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='faq_questions', null=True, to=orm['cms.Placeholder'])),
        ))
        db.send_create_signal(u'aldryn_faq', ['Question'])


    def backwards(self, orm):
        # Removing unique constraint on 'CategoryTranslation', fields ['language_code', 'master']
        db.delete_unique(u'aldryn_faq_category_translation', ['language_code', 'master_id'])

        # Deleting model 'CategoryTranslation'
        db.delete_table(u'aldryn_faq_category_translation')

        # Deleting model 'Category'
        db.delete_table(u'aldryn_faq_category')

        # Deleting model 'Question'
        db.delete_table(u'aldryn_faq_question')


    models = {
        u'aldryn_faq.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'aldryn_faq.categorytranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'CategoryTranslation', 'db_table': "u'aldryn_faq_category_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_faq.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'aldryn_faq.question': {
            'Meta': {'ordering': "['order']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faq_questions'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'category': ('adminsortable.fields.SortableForeignKey', [], {'to': u"orm['aldryn_faq.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_faq']