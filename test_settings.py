# -*- coding: utf-8 -*-

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
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_faq')

if __name__ == "__main__":
    run()
