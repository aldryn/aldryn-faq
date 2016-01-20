# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration

from django.conf import settings
from django.db import models, connection, transaction


def create_placeholders(app_config, orm):
    """
    Creates placeholder instances for each Placeholder field on provided
    app_config.
    """
    from cms.models import Placeholder

    for field in app_config._meta.fields:
        if field.__class__ != models.fields.related.ForeignKey:
            # skip not FK fields
            continue

        if not (field.rel.to == Placeholder or
                field.rel.to == orm['cms.Placeholder']):
            # skip other fields.
            continue

        placeholder_name = field.name
        # south doesn't keeps the field.slotname, so we have to pick it
        # up from field.name
        slot_name = placeholder_name.replace('placeholder_', '')
        placeholder_id_name = '{0}_id'.format(placeholder_name)
        placeholder_id = getattr(app_config, placeholder_id_name, None)
        if placeholder_id is not None:
            # do not process if it has a reference to placeholder field.
            continue
        # since there is no placeholder - create it, we cannot use
        # get_or_create because it can get placeholder from other config
        new_placeholder = Placeholder.objects.create(
            slot=slot_name)
        setattr(app_config, placeholder_id_name, new_placeholder.pk)
    # after we process all placeholder fields - save config,
    # so that django can pick up them.
    app_config.save()


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        if connection.vendor == 'sqlite':
            transaction.set_autocommit(True)
        FaqConfig = orm.FaqConfig
        Category = orm.Category
        app_config_count = FaqConfig.objects.count()
        app_config, created = FaqConfig.objects.get_or_create(
            namespace='aldryn_faq_default')

        if created:
            app_config_translation = app_config.translations.create()
            app_config_translation.language_code = settings.LANGUAGES[0][0]
            app_config_translation.app_title = 'Default FAQ'
            app_config_translation.save()

        # set app config for categoris only if there were
        # no other existing app configs.
        if app_config_count == 0:
            for entry in Category.objects.filter(appconfig__isnull=True):
                entry.appconfig = app_config
                entry.save()

        # create all missing placeholders
        for cfg in FaqConfig.objects.all():
            create_placeholders(cfg, orm)

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        u'aldryn_faq.category': {
            'Meta': {'object_name': 'Category'},
            'appconfig': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_faq.FaqConfig']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'aldryn_faq.faqconfig': {
            'Meta': {'object_name': 'FaqConfig'},
            'app_data': ('app_data.fields.AppDataField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '100'}),
            'non_permalink_handling': ('django.db.models.fields.SmallIntegerField', [], {'default': '302'}),
            'permalink_type': ('django.db.models.fields.CharField', [], {'default': "u'Ss'", 'max_length': '2'}),
            'placeholder_faq_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'aldryn_faq_content'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'placeholder_faq_list_bottom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'aldryn_faq_list_bottom'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'placeholder_faq_list_top': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'aldryn_faq_list_top'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'placeholder_faq_sidebar_bottom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'aldryn_faq_sidebar_bottom'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'placeholder_faq_sidebar_top': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'aldryn_faq_sidebar_top'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
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
            'Meta': {'ordering': "(u'order',)", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'faq_questions'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'questions'", 'to': u"orm['aldryn_faq.Category']"}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'aldryn_faq.selectedcategory': {
            'Meta': {'ordering': "[u'position']", 'object_name': 'SelectedCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_faq.Category']"}),
            'cms_plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'selected_categories'", 'to': u"orm['aldryn_faq.CategoryListPlugin']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
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
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_faq']
    symmetrical = True
