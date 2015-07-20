# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('aldryn_faq', '0004_auto_20150626_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questiontranslation',
            name='answer_text',
            field=djangocms_text_ckeditor.fields.HTMLField(verbose_name='Short description'),
            preserve_default=True,
        ),
    ]
