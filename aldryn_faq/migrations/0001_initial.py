# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations, transaction
from django.db.models import get_model
from django.db.utils import ProgrammingError, OperationalError
import aldryn_translation_tools.models
import app_data.fields
import cms.models.fields
import sortedm2m.fields
import djangocms_text_ckeditor.fields

APP_PACKAGE = 'aldryn_faq'
APP_CONFIG = 'FaqConfig'
DEFAULT_NAMESPACE = 'aldryn_faq_default'
DEFAULT_APP_TITLE = 'Default FAQ'


def noop(apps, schema_editor):
    pass


def get_config_count(model_class):
    with transaction.atomic():
        count = model_class.objects.count()
    return count


def create_default_config(apps, schema_editor):
    FaqConfig = apps.get_model(APP_PACKAGE, APP_CONFIG)

    # if we try to execute this migration after cms migrations were migrated
    # to latest - we would get an exception because apps.get_model
    # contains cms models in the last known state (which is the dependency
    # migration state). If that is the case we need to import the real model.
    try:
        # to avoid the following error:
        #   django.db.utils.InternalError: current transaction is aborted,
        #   commands ignored until end of transaction block
        # we need to cleanup or avoid that by making transaction atomic.
        count = get_config_count(FaqConfig)
    except (ProgrammingError, OperationalError):
        model_path = '{0}.{1}'.format(APP_PACKAGE, APP_CONFIG)
        FaqConfig = get_model(model_path)
        count = get_config_count(FaqConfig)

    if not count == 0:
        return
    # create only if there is no configs because user may already have
    # existing and configured config.
    app_config = FaqConfig(namespace=DEFAULT_NAMESPACE)
    # usually generated in aldryn_apphooks_config.models.AppHookConfig
    # but in migrations we don't have real class with correct parents.
    app_config.type = '{0}.cms_appconfig.{1}'.format(APP_PACKAGE, APP_CONFIG)
    # placeholders
    # cms checks if instance.pk is set, and if it isn't cms creates a new
    # placeholder but it does that with real models, and fields on instance
    # are faked models. To prevent that we need to manually set instance pk.
    app_config.pk = 1
    app_config.save()

    # translations
    app_config_translation = app_config.translations.create()
    app_config_translation.language_code = settings.LANGUAGES[0][0]
    app_config_translation.app_title = DEFAULT_APP_TITLE
    app_config_translation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CategoryListPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_faq.Category', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'aldryn_faq_category_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'category Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='type')),
                ('namespace', models.CharField(default=None, unique=True, max_length=100, verbose_name='instance namespace')),
                ('app_data', app_data.fields.AppDataField(default=dict, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqConfigTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('app_title', models.CharField(max_length=234, verbose_name='application title')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_faq.FaqConfig', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'aldryn_faq_faqconfig_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'faq config Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestQuestionsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('questions', models.IntegerField(default=5, help_text='The number of questions to be displayed.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.CreateModel(
            name='MostReadQuestionsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('questions', models.IntegerField(default=5, help_text='The number of questions to be displayed.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_top', models.BooleanField(default=False)),
                ('number_of_visits', models.PositiveIntegerField(default=0, editable=False)),
                ('order', models.PositiveIntegerField(default=1, db_index=True)),
                ('answer', cms.models.fields.PlaceholderField(related_name='faq_questions', slotname='faq_question_answer', editable=False, to='cms.Placeholder', null=True)),
                ('category', models.ForeignKey(related_name='questions', to='aldryn_faq.Category')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionListPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('questions', sortedm2m.fields.SortedManyToManyField(help_text=None, to='aldryn_faq.Question')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='QuestionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('answer_text', djangocms_text_ckeditor.fields.HTMLField(verbose_name='answer')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_faq.Question', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'aldryn_faq_question_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'question Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SelectedCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='position', blank=True)),
                ('category', models.ForeignKey(verbose_name='category', to='aldryn_faq.Category')),
                ('cms_plugin', models.ForeignKey(related_name='selected_categories', to='aldryn_faq.CategoryListPlugin')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopQuestionsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('questions', models.IntegerField(default=5, help_text='The number of questions to be displayed.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='questiontranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='faqconfigtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='category',
            name='appconfig',
            field=models.ForeignKey(verbose_name='appconfig', blank=True, to='aldryn_faq.FaqConfig', null=True),
            preserve_default=True,
        ),
        # create default FaqConfig
        migrations.RunPython(create_default_config, noop)
    ]
