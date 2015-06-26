# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
        ('aldryn_faq', '0003_preset_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqconfig',
            name='placeholder_faq_content',
            field=cms.models.fields.PlaceholderField(related_name='aldryn_faq_content', slotname='faq_content', editable=False, to='cms.Placeholder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='placeholder_faq_list_bottom',
            field=cms.models.fields.PlaceholderField(related_name='aldryn_faq_list_bottom', slotname='faq_list_bottom', editable=False, to='cms.Placeholder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='placeholder_faq_list_top',
            field=cms.models.fields.PlaceholderField(related_name='aldryn_faq_list_top', slotname='faq_list_top', editable=False, to='cms.Placeholder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='placeholder_faq_sidebar_bottom',
            field=cms.models.fields.PlaceholderField(related_name='aldryn_faq_sidebar_bottom', slotname='faq_sidebar_bottom', editable=False, to='cms.Placeholder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqconfig',
            name='placeholder_faq_sidebar_top',
            field=cms.models.fields.PlaceholderField(related_name='aldryn_faq_sidebar_top', slotname='faq_sidebar_top', editable=False, to='cms.Placeholder', null=True),
            preserve_default=True,
        ),
    ]
