# -*- coding: utf-8 -*-

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
        'aldryn_boilerplates',
        'aldryn_faq',
        'aldryn_reversion',
        'aldryn_translation_tools',
        'djangocms_text_ckeditor',
        'parler',
        'reversion',
        'sortedm2m',

        # NOTE: The following is NOT required for new installs, it is, however,
        # required for testing the migrations.
        'adminsortable',
    ],
    'MIGRATION_MODULES': {
        'cms': 'cms.migrations_django',
        'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
    },
    'STATICFILES_FINDERS': [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # important! place right before django.contrib.staticfiles.finders.AppDirectoriesFinder
        'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ],
    'TEMPLATE_LOADERS': [
        'django.template.loaders.filesystem.Loader',
        # important! place right before django.template.loaders.app_directories.Loader
        'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
        'django.template.loaders.app_directories.Loader',
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
                'name': 'Français',
                'fallbacks': ['en', ]
            },
        ],
        'default': {
            'hide_untranslated': False,
        }
    },
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_faq')

if __name__ == "__main__":
    run()
