# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app_data.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0009_auto_20160107_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqconfig',
            name='app_data',
            field=app_data.fields.AppDataField(default='{}', editable=False),
        ),
    ]
