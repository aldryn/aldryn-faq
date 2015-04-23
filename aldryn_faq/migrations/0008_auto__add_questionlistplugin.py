# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from aldryn_faq.utils import rename_tables_new_to_old


class Migration(SchemaMigration):

    def forwards(self, orm):
        rename_tables_new_to_old(db)

        # Adding model 'QuestionListPlugin'
        db.create_table(u'cmsplugin_questionlistplugin', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'aldryn_faq', ['QuestionListPlugin'])


        # Adding SortedM2M table for field questions on 'QuestionListPlugin'
        db.create_table(u'aldryn_faq_questionlistplugin_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionlistplugin', models.ForeignKey(orm[u'aldryn_faq.questionlistplugin'], null=False)),
            ('question', models.ForeignKey(orm[u'aldryn_faq.question'], null=False)),
            ('sort_value', models.IntegerField())
        ))
        db.create_unique(u'aldryn_faq_questionlistplugin_questions', ['questionlistplugin_id', 'question_id'])

    def backwards(self, orm):
        rename_tables_new_to_old(db)

        # Deleting model 'QuestionListPlugin'
        db.delete_table(u'cmsplugin_questionlistplugin')

        # Removing M2M table for field questions on 'QuestionListPlugin'
        db.delete_table(db.shorten_name(u'cmsplugin_questionlistplugin_questions'))


    models = {
        u'aldryn_faq.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'aldryn_faq.categorylistplugin': {
            'Meta': {'object_name': 'CategoryListPlugin', 'db_table': "u'cmsplugin_categorylistplugin'", '_ormbases': ['cms.CMSPlugin']},
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
            'Meta': {'object_name': 'LatestQuestionsPlugin', 'db_table': "u'cmsplugin_latestquestionsplugin'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        u'aldryn_faq.question': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faq_questions'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'answer_text': ('djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('adminsortable.fields.SortableForeignKey', [], {'related_name': "'questions'", 'to': u"orm['aldryn_faq.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'aldryn_faq.questionlistplugin': {
            'Meta': {'object_name': 'QuestionListPlugin', 'db_table': "u'cmsplugin_questionlistplugin'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'questions': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['aldryn_faq.Question']", 'symmetrical': 'False'})
        },
        u'aldryn_faq.selectedcategory': {
            'Meta': {'ordering': "['position']", 'object_name': 'SelectedCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_faq.Category']"}),
            'cms_plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selected_categories'", 'to': u"orm['aldryn_faq.CategoryListPlugin']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'aldryn_faq.topquestionsplugin': {
            'Meta': {'object_name': 'TopQuestionsPlugin', 'db_table': "u'cmsplugin_topquestionsplugin'", '_ormbases': ['cms.CMSPlugin']},
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