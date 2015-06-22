# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_faq import __version__

REQUIREMENTS = [
    'aldryn-apphooks-config',
    'aldryn-reversion',
    'aldryn-search',
    'aldryn-translation-tools',
    'django-admin-sortable',  # DO NOT REMOVE THIS
    'django-admin-sortable2>=0.5.0',
    'django-parler',
    'django-sortedm2m',
    'django-cms>=3.0.12',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
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
    include_package_data=True,
    zip_safe=False
)
