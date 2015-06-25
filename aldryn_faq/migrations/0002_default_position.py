# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedcategory',
            name='position',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='position', blank=True),
            preserve_default=True,
        ),
    ]
