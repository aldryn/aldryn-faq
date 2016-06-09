# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from aldryn_faq import __version__

py26 = (2, 7, 0) > sys.version_info >= (2, 6, 0)

REQUIREMENTS = [
    'aldryn-apphooks-config>=0.2.4',
    'aldryn-boilerplates>=0.7.4,<0.8',
    'aldryn-reversion>=1.0.4,<1.1',
    'aldryn-search',
    'aldryn-translation-tools>=0.2.1',
    'django>=1.6,<1.9.999',
    'django-admin-sortable2>=0.5.2',
    'django-cms>=3.0.12,<3.4',
    'djangocms-text-ckeditor',
    'django-parler>=1.4,<1.7',
    'django-reversion>=1.8.2,<1.11',
    'django-sortedm2m>=1.2.2',

    # THIS IS HERE TO SUPPORT EXISTING MIGRATIONS AND CAN BE REMOVED ONLY ONCE
    # WE NO LONGER SUPPORT SOUTH MIGRATIONS.
    'django-admin-sortable',
]

# use appropriate 3rd party packages versions
if py26:
    REQUIREMENTS += [
        'django-taggit<0.18.0',
    ]
else:
    REQUIREMENTS += [
        'django-taggit',
    ]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.6',
    'Framework :: Django :: 1.7',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-faq',
    version=__version__,
    description='FAQ addon for django CMS',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-faq',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
