# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from distutils.version import LooseVersion
from cms import __version__ as cms_string_version

cms_version = LooseVersion(cms_string_version)


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:9001/solr/default',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    },
    'en': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://my-solr-server/solr/my-site-en/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
    'de': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://my-solr-server/solr/my-site-de/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
    ),
    'CMS_PERMISSION': True,
    'INSTALLED_APPS': [
        'adminsortable2',
        'aldryn_reversion',
        'aldryn_translation_tools',
        'djangocms_text_ckeditor',
        'parler',
        'reversion',
        'sortedm2m',
        'taggit',

        # NOTE: The following is NOT required for new installs, it is, however,
        # required for testing the migrations.
        'adminsortable',
    ],
    'MIDDLEWARE_CLASSES': [
        'cms.middleware.utils.ApphookReloadMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware'
    ],
    'HAYSTACK_CONNECTIONS': HAYSTACK_CONNECTIONS,
    'PARLER_LANGUAGES': {
        1: (
            {'code': 'de', },
            {'code': 'en', },
            {'code': 'fr', },
        ),
        'default': {
            'hide_untranslated': False,
        }
    },
    'PARLER_ENABLE_CACHING': False,
    'SITE_ID': 1,
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'de',
                'name': 'Deutsche',
                'fallbacks': ['en', ]
            },
            {
                'code': 'en',
                'name': 'English',
                'fallbacks': ['de', ]
            },
            {
                'code': 'fr',
                'name': 'French',
                'fallbacks': ['en', ]
            },
        ],
        'default': {
            'hide_untranslated': False,
        }
    },
    'SOUTH_MIGRATION_MODULES': {
        'taggit': 'taggit.south_migrations',
    }
}

# If using CMS 3.2+, use the CMS middleware for ApphookReloading, otherwise,
# use aldryn_apphook_reload's.
if cms_version < LooseVersion('3.2.0'):
    HELPER_SETTINGS['INSTALLED_APPS'].insert(0, 'aldryn_apphook_reload'),
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'].remove(
        'cms.middleware.utils.ApphookReloadMiddleware')
    HELPER_SETTINGS['MIDDLEWARE_CLASSES'].insert(
        0, 'aldryn_apphook_reload.middleware.ApphookReloadMiddleware')


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_faq', extra_args=[])


if __name__ == "__main__":
    run()
