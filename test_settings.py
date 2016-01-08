# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    'INSTALLED_APPS': [
        'adminsortable2',
        'aldryn_apphook_reload',
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
    # This set of MW classes should work for Django 1.6 and 1.7.
    'MIDDLEWARE_CLASSES': [
        'aldryn_apphook_reload.middleware.ApphookReloadMiddleware',
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
    'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
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
                'name': u'Française',
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


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_faq', extra_args=['--boilerplate'])

if __name__ == "__main__":
    run()
