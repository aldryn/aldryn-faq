# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from parler.utils.context import switch_language

# we need to use real models since otherwise fake class is provided
# by Django, which doesn't has any parler methods.
from aldryn_faq.models import Question


def resave_questions_for_slug_autogeneration(apps, schema_editor):
    """Trigger save method for each existing Question to generate slug"""
    for question in Question.objects.all():
        for translation in question.translations.all():
            with switch_language(question,
                                 language_code=translation.language_code):
                question.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0007_auto_20150903_1503'),
    ]

    operations = [
        migrations.RunPython(resave_questions_for_slug_autogeneration, do_nothing),
    ]
