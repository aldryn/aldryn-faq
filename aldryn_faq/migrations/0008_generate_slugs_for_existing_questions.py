# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.utils.text import slugify
from django.utils.encoding import force_text

from aldryn_translation_tools.models import TranslatedAutoSlugifyMixin


class AutoSlugifyQuestions(TranslatedAutoSlugifyMixin):
    slug_max_length = 255
    slug_source_field_name = 'title'

    def __init__(self, translation, query_model=None):
        self.translation = translation
        self.query_model = query_model

    # override some methods since we are performing operaions on the translation
    # not the question itself.
    def get_slug_source(self):
        return getattr(self.translation, self.slug_source_field_name, None)

    def _get_existing_slug(self):
        getattr(self.translation, self.slug_field_name, None)

    def _get_slug_queryset(self, lookup_model=None):
        return super(AutoSlugifyQuestions, self)._get_slug_queryset(
            lookup_model=self.query_model)

    def get_current_language(self):
        return self.translation.language_code


def resave_questions_for_slug_autogeneration(apps, schema_editor):
    """Trigger save method for each existing Question to generate slug"""
    Question = apps.get_model("aldryn_faq", "Question")
    for question in Question.objects.all():
        for translation in question.translations.all():
            AutoSlugify = AutoSlugifyQuestions(translation)
            translation.slug = AutoSlugify.make_new_slug(
                qs=Question.objects.all())
            translation.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0007_auto_20150903_1503'),
    ]

    operations = [
        migrations.RunPython(resave_questions_for_slug_autogeneration, do_nothing),
    ]
