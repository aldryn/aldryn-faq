# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def preset_order(apps, schema_editor):
    """Set initial ordering of category list plugin categories."""
    SelectedCategory = apps.get_model("aldryn_faq", "SelectedCategory")
    order = 0
    for obj in SelectedCategory.objects.all():
        order += 1
        obj.position = order
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_faq', '0002_default_position'),
    ]

    operations = [
        migrations.RunPython(preset_order),
    ]
