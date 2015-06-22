# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from aldryn_faq.utils import rename_tables_new_to_old


class Migration(SchemaMigration):

    def forwards(self, orm):
        rename_tables_new_to_old(db)

        # Adding model 'FaqConfigTranslation'
        db.create_table(u'aldryn_faq_faqconfig_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('app_title', self.gf('django.db.models.fields.CharField')(max_length=234)),
            (u'master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['aldryn_faq.FaqConfig'])),
        ))
        db.send_create_signal(u'aldryn_faq', ['FaqConfigTranslation'])

        # Adding unique constraint on 'FaqConfigTranslation', fields ['language_code', u'master']
        db.create_unique(u'aldryn_faq_faqconfig_translation', ['language_code', u'master_id'])

        # Adding model 'FaqConfig'
        db.create_table(u'aldryn_faq_faqconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('namespace', self.gf('django.db.models.fields.CharField')(default=None, max_length=100)),
            ('app_data', self.gf('app_data.fields.AppDataField')(default='{}')),
        ))
        db.send_create_signal(u'aldryn_faq', ['FaqConfig'])

        # Adding field 'Category.namespace'
        db.add_column(u'aldryn_faq_category', 'namespace',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, null=True, to=orm['aldryn_faq.FaqConfig']),
                      keep_default=False)


    def backwards(self, orm):
        rename_tables_new_to_old(db)

        # Removing unique constraint on 'FaqConfigTranslation', fields ['language_code', u'master']
        db.delete_unique(u'aldryn_faq_faqconfig_translation', ['language_code', u'master_id'])

        # Deleting model 'FaqConfigTranslation'
        db.delete_table(u'aldryn_faq_faqconfig_translation')

        # Deleting model 'FaqConfig'
        db.delete_table(u'aldryn_faq_faqconfig')

        # Deleting field 'Category.namespace'
        db.delete_column(u'aldryn_faq_category', 'namespace_id')


    models = {
        u'aldryn_faq.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_faq.FaqConfig']"})
        },
        u'aldryn_faq.categorylistplugin': {
            'Meta': {'object_name': 'CategoryListPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'aldryn_faq.categorytranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'master')]", 'object_name': 'CategoryTranslation', 'db_table': "u'aldryn_faq_category_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_faq.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'aldryn_faq.faqconfig': {
            'Meta': {'object_name': 'FaqConfig'},
            'app_data': ('app_data.fields.AppDataField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'aldryn_faq.faqconfigtranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'master')]", 'object_name': 'FaqConfigTranslation', 'db_table': "u'aldryn_faq_faqconfig_translation'"},
            'app_title': ('django.db.models.fields.CharField', [], {'max_length': '234'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_faq.FaqConfig']"})
        },
        u'aldryn_faq.latestquestionsplugin': {
            'Meta': {'object_name': 'LatestQuestionsPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        u'aldryn_faq.mostreadquestionsplugin': {
            'Meta': {'object_name': 'MostReadQuestionsPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        u'aldryn_faq.question': {
            'Meta': {'ordering': "['order']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'faq_questions'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'category': ('adminsortable.fields.SortableForeignKey', [], {'related_name': "u'questions'", 'to': u"orm['aldryn_faq.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_visits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        u'aldryn_faq.questionlistplugin': {
            'Meta': {'object_name': 'QuestionListPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['aldryn_faq.Question']", 'symmetrical': 'False'})
        },
        u'aldryn_faq.questiontranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'master')]", 'object_name': 'QuestionTranslation', 'db_table': "u'aldryn_faq_question_translation'"},
            'answer_text': ('djangocms_text_ckeditor.fields.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_faq.Question']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'aldryn_faq.selectedcategory': {
            'Meta': {'ordering': "[u'position']", 'object_name': 'SelectedCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_faq.Category']"}),
            'cms_plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'selected_categories'", 'to': u"orm['aldryn_faq.CategoryListPlugin']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'aldryn_faq.topquestionsplugin': {
            'Meta': {'object_name': 'TopQuestionsPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_faq']