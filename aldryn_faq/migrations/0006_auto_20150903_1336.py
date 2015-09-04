# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0005_auto_20150720_1344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faqconfig',
            options={'verbose_name': 'config', 'verbose_name_plural': 'configs'},
        ),
        migrations.AlterModelOptions(
            name='faqconfigtranslation',
            options={'default_permissions': (), 'verbose_name': 'config Translation', 'managed': True},
        ),
        migrations.AddField(
            model_name='questiontranslation',
            name='slug',
            field=models.SlugField(help_text='Provide a "slug" for this category or leave blank for an auto-generated one.', max_length=255, verbose_name='Slug', blank=True),
        ),
        migrations.AlterField(
            model_name='categorytranslation',
            name='slug',
            field=models.SlugField(help_text='Provide a "slug" for this category or leave blank for an auto-generated one.', max_length=255, verbose_name='Slug', blank=True),
        ),
    ]
