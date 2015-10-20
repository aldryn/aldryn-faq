# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.utils.text import slugify
from django.utils.encoding import force_text


def get_slug_candidate(question_model, translation, language_code):
    """
    Generate the slug candidate the same way as
    aldryn-translation-tools.TranslatedAutoSlugifyMixin does that.
    Simplified, since we know in advance
    """
    if not getattr(translation, 'slug', ''):
        slug_source = translation.title
        slug = force_text(slugify(slug_source))
        candidate = force_text(slugify(slug_source))
        qs = question_model.objects.filter(
            translations__language_code=language_code).exclude(
            pk=translation.master_id)
        idx = 1

        while qs.filter(translations__slug=candidate).exists():
            # at this point max length for
            if len(candidate) > 255:
                slug = slug[:255-len(str(idx))]
            candidate = "{slug}-{idx}".format(slug=slug, idx=idx)
            idx += 1
        return candidate


def resave_questions_for_slug_autogeneration(apps, schema_editor):
    """Trigger save method for each existing Question to generate slug"""
    Question = apps.get_model("aldryn_faq", "Question")
    for question in Question.objects.all():
        for translation in question.translations.all():
            translation.slug = get_slug_candidate(Question, translation,
                                                  translation.language_code)
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
