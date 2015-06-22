# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from aldryn_faq.utils import rename_tables_new_to_old


class Migration(SchemaMigration):

    def forwards(self, orm):
        rename_tables_new_to_old(db)

        # Deleting field 'Question.answer_text'
        db.delete_column(u'aldryn_faq_question', 'answer_text')

        # Deleting field 'Question.language'
        db.delete_column(u'aldryn_faq_question', 'language')

        # Deleting field 'Question.title'
        db.delete_column(u'aldryn_faq_question', 'title')


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration. 'Question.language' and its values cannot be restored.")

        rename_tables_new_to_old(db)

        # Adding field 'Question.answer_text'
        db.add_column(u'aldryn_faq_question', 'answer_text',
                      self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True),
                      keep_default=False)
        # User chose to not deal with backwards NULL issues for 'Question.language'
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Question.language'
        db.add_column(u'aldryn_faq_question', 'language',
                      self.gf('django.db.models.fields.CharField')(max_length=5),
                      keep_default=False)


    models = {
        u'aldryn_faq.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'aldryn_faq.categorylistplugin': {
            'Meta': {'object_name': 'CategoryListPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'aldryn_faq.categorytranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'CategoryTranslation', 'db_table': "u'aldryn_faq_category_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_faq.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'aldryn_faq.latestquestionsplugin': {
            'Meta': {'object_name': 'LatestQuestionsPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        u'aldryn_faq.question': {
            'Meta': {'ordering': "['order']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faq_questions'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'category': ('adminsortable.fields.SortableForeignKey', [], {'related_name': "'questions'", 'to': u"orm['aldryn_faq.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        u'aldryn_faq.questionlistplugin': {
            'Meta': {'object_name': 'QuestionListPlugin', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['aldryn_faq.Question']", 'symmetrical': 'False'})
        },
        u'aldryn_faq.questiontranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'QuestionTranslation', 'db_table': "u'aldryn_faq_question_translation'"},
            'answer_text': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_faq.Question']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'aldryn_faq.selectedcategory': {
            'Meta': {'ordering': "['position']", 'object_name': 'SelectedCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_faq.Category']"}),
            'cms_plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selected_categories'", 'to': u"orm['aldryn_faq.CategoryListPlugin']"}),
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
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_faq']