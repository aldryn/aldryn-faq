# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0008_generate_slugs_for_existing_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytranslation',
            name='name',
            field=models.CharField(help_text='Provide the category\u2019s name', max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='questiontranslation',
            name='title',
            field=models.CharField(help_text='This should be a short form of the question', max_length=255, verbose_name='Title'),
        ),
    ]
