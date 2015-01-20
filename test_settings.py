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
    'ROOT_URLCONF': 'aldryn_faq.tests.urls',
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
    ),
    'INSTALLED_APPS': [
        'adminsortable',
        'aldryn_faq',
        'djangocms_text_ckeditor',
        'hvad',
        'sortedm2m',
    ],
    "HAYSTACK_CONNECTIONS": HAYSTACK_CONNECTIONS
}


def run():
    import sys
    from djangocms_helper import runner
    if len(sys.argv) == 1:
        sys.argv.append('test')
    sys.argv.append('--extra-settings=test_settings.py')
    runner.cms('aldryn_faq')

if __name__ == "__main__":
    run()
