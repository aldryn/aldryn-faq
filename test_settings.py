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
    import sys
    from djangocms_helper import runner
    if len(sys.argv) == 1:
        sys.argv.append('test')
    sys.argv.append('--extra-settings=test_settings.py')
    runner.cms('aldryn_faq')

if __name__ == "__main__":
    run()
