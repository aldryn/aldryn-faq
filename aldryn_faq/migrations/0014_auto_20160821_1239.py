# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0013_auto_20160623_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorylistplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='aldryn_faq_categorylistplugin', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='latestquestionsplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='aldryn_faq_latestquestionsplugin', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='mostreadquestionsplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='aldryn_faq_mostreadquestionsplugin', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='questionlistplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='aldryn_faq_questionlistplugin', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='topquestionsplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='aldryn_faq_topquestionsplugin', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]
