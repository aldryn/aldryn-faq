# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
        ('aldryn_faq', '0011_create_default_faq_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorytranslation',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(default='', help_text='Optional. Description of this category.', verbose_name='description', blank=True),
            preserve_default=True,
        ),
    ]
