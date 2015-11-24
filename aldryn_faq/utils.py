# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse, NoReverseMatch

default_cms_plugin_table_mapping = (
    # (old_name, new_name),
    ('cmsplugin_categorylistplugin', 'aldryn_faq_categorylistplugin'),
    ('cmsplugin_latestquestionsplugin', 'aldryn_faq_latestquestionsplugin'),
    ('cmsplugin_mostreadquestionsplugin',
     'aldryn_faq_mostreadquestionsplugin'),
    ('cmsplugin_questionlistplugin', 'aldryn_faq_questionlistplugin'),
    ('cmsplugin_questionlistplugin_questions',
     'aldryn_faq_questionlistplugin_questions'),
    ('cmsplugin_topquestionsplugin', 'aldryn_faq_topquestionsplugin'),
)


def rename_tables(db, table_mapping=None, reverse=False):
    """
    renames tables from source to destination name, if the source exists
    and the destination does not exist yet.

    taken from cmsplugin-filer:cmsplugin_filer_utils.migration
    (thanks to @stefanfoulis)
    """
    from django.db import connection

    if not table_mapping:
        table_mapping = default_cms_plugin_table_mapping

    if reverse:
        table_mapping = [(dst, src) for src, dst in table_mapping]
    table_names = connection.introspection.table_names()
    for source, destination in table_mapping:
        if source in table_names and destination in table_names:
            print("    WARNING: not renaming {0} to {1}, because both "
                  "tables already exist.".format(source, destination))
        elif source in table_names and destination not in table_names:
            print("     - renaming {0} to {1}".format(source, destination))
            db.rename_table(source, destination)


def rename_tables_old_to_new(db, table_mapping=None):
    return rename_tables(db, table_mapping, reverse=False)


def rename_tables_new_to_old(db, table_mapping=None):
    return rename_tables(db, table_mapping, reverse=True)


def is_valid_namespace(namespace):
    """
    Check if provided namespace has an app-hooked page.
    Returns True or False.
    """
    try:
        reverse('{0}:faq-category-list'.format(namespace))
    except (NoReverseMatch, AttributeError):
        return False
    return True


def is_valid_app_config(app_config):
    """
    Checks if provided app_config is valid. Tries to get namespace.
    """
    return getattr(app_config, 'namespace', None)
