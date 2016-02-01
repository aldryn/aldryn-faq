# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations, transaction
from django.apps import apps as django_apps
from django.db.utils import ProgrammingError, OperationalError

APP_PACKAGE = 'aldryn_faq'
APP_CONFIG = 'FaqConfig'
DEFAULT_NAMESPACE = 'aldryn_faq_default'
DEFAULT_APP_TITLE = 'Default FAQ'


def noop(apps, schema_editor):
    pass


def get_config_count(model_class):
    with transaction.atomic():
        count = model_class.objects.count()
    return count


def create_placeholders(app_config, save=True):
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
            slot=field.slotname)
        setattr(app_config, placeholder_id_name, new_placeholder.pk)
    # after we process all placeholder fields - save config,
    # so that django can pick up them.
    if save:
        app_config.save()


def create_default_config(apps, schema_editor):
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
        count = get_config_count(FaqConfig)
    except (ProgrammingError, OperationalError):
        model_path = '{0}.{1}'.format(APP_PACKAGE, APP_CONFIG)
        FaqConfig = django_apps.get_model(model_path)
        count = get_config_count(FaqConfig)

    if not count == 0:
        for cfg in FaqConfig.objects.all():
            create_placeholders(cfg)
        return
    # create only if there is no configs because user may already have
    # existing and configured config.
    app_config = FaqConfig(namespace=DEFAULT_NAMESPACE)
    # usually generated in aldryn_apphooks_config.models.AppHookConfig
    # but in migrations we don't have real class with correct parents.
    app_config.type = '{0}.cms_appconfig.{1}'.format(APP_PACKAGE, APP_CONFIG)
    # placeholders
    # cms checks if instance.pk is set, and if it isn't cms creates a new
    # placeholder but it does that with real models, and fields on instance
    # are faked models. To prevent that we need to manually set instance pk.
    app_config.pk = 1
    # placeholders
    create_placeholders(app_config, save=False)
    app_config.save()

    # translations
    app_config_translation = app_config.translations.create()
    app_config_translation.language_code = settings.LANGUAGES[0][0]
    app_config_translation.app_title = DEFAULT_APP_TITLE
    app_config_translation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
        ('aldryn_faq', '0010_auto_20160109_2144')
    ]

    operations = [
        migrations.RunPython(create_default_config, noop)
    ]
