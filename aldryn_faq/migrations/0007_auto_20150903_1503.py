# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0006_auto_20150903_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqconfig',
            name='non_permalink_handling',
            field=models.SmallIntegerField(default=302, help_text='How to handle non-permalink urls?', verbose_name='non-permalink handling', choices=[(200, 'Allow'), (302, 'Redirect to permalink (default)'), (301, 'Permanent redirect to permalink'), (404, 'Return 404: Not Found')]),
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='permalink_type',
            field=models.CharField(default='Ss', help_text='Choose the style of urls to use from the examples. (Note, all types are relative to apphook)', max_length=2, verbose_name='permalink type', choices=[('Pp', '1/2/'), ('Ps', '1/question-slug/'), ('Sp', 'category-slug/2/'), ('Ss', 'category-slug/question-slug/'), ('Bp', '1-category-slug/2/'), ('Bs', '1-category-slug/question-slug/')]),
        ),
    ]
