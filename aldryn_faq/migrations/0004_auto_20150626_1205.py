# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction
from django.db.models import get_model
from django.db.utils import ProgrammingError, OperationalError
import cms.models.fields

APP_PACKAGE = 'aldryn_faq'
APP_CONFIG = 'FaqConfig'


def noop(apps, schema_editor):
    pass


def get_configs(model_class):
    with transaction.atomic():
        app_configs = list(model_class.objects.all())
    return app_configs


def create_placeholders(app_config):
    """
    Creates placeholder instances for each Placeholder field on provided
    app_config.
    """
    import cms.models.fields
    from cms.models import Placeholder

    for field in app_config._meta.fields:
        if not field.__class__ == cms.models.fields.PlaceholderField:
            # skip other fields.
            continue
        placeholder_name = field.name
        placeholder_id_name = '{0}_id'.format(placeholder_name)
        placeholder_id = getattr(app_config, placeholder_id_name, None)
        if placeholder_id is not None:
            # do not process if it has a reference to placeholder field.
            continue
        # since there is no placeholder - create it, we cannot use
        # get_or_create because it can get placeholder from other config
        new_placeholder = Placeholder.objects.create(
            slot=placeholder_name)
        setattr(app_config, placeholder_id_name, new_placeholder.pk)
    # after we process all placeholder fields - save config,
    # so that django can pick up them.
    app_config.save()


def create_placeholders_for_app_configs(apps, schema_editor):
    FaqConfig = apps.get_model(APP_PACKAGE, APP_CONFIG)
    # if we try to execute this migration after cms migrations were migrated
    # to latest - we would get an exception because apps.get_model
    # contains cms models in the last known state (which is the dependency
    # migration state). If that is the case we need to import the real model.
    try:
        # to avoid the following error:
        #   django.db.utils.InternalError: current transaction is aborted,
        #   commands ignored until end of transaction block
        # we need to cleanup or avoid that by making transaction atomic.
        app_configs = get_configs(FaqConfig)
    except (ProgrammingError, OperationalError):
        model_path = '{0}.{1}'.format(APP_PACKAGE, APP_CONFIG)
        FaqConfig = get_model(model_path)
        app_configs = get_configs(FaqConfig)

    if not app_configs:
        return

    for app_config in app_configs:
        create_placeholders(app_config)


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
        # create default FaqConfig placeholders
        migrations.RunPython(create_placeholders_for_app_configs, noop)
    ]
