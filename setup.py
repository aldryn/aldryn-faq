# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_faq import __version__

REQUIREMENTS = [
    'aldryn-apphooks-config>=0.2.4',
    'aldryn-reversion>=0.0.2,<0.1.0',
    'aldryn-search',
    'aldryn-translation-tools>=0.0.5,<0.0.7',
    'django>=1.6,<1.8',
    'django-admin-sortable2>=0.5.2',
    'django-cms>=3.0.12,<3.2',
    'django-parler>=1.4',
    'django-reversion>=1.8.2,<1.9',
    'django-sortedm2m',
    'django-parler',

    # THIS IS HERE TO SUPPORT EXISTING MIGRATIONS AND CAN BE REMOVED ONLY ONCE
    # WE NO LONGER SUPPORT SOUTH MIGRATIONS.
    'django-admin-sortable',
]

DEPENDENCY_LINKS = [
    # THIS CAN BE REMOVED ONCE THERE IS A RELEASE > 1.4.0
    'git+https://github.com/edoburu/django-parler@9d25bc60b24a16bc4781d0305c41c5acff0b00a6#egg=django-parler',
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.6',
    'Framework :: Django :: 1.7',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
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
    dependency_links=DEPENDENCY_LINKS,
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
