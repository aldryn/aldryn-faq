############
Installation
############

You can install Aldryn FAQ either on `Aldryn <http://www.aldryn.com>`_
or by hand into your own project.


*********************
Aldryn Platform Users
*********************

To install the addon on Aldryn, all you need to do is follow this
`installation link <https://control.aldryn.com/control/?select_project_for_addon=aldryn-faq>`_
on the Aldryn Marketplace and follow the instructions.

Manually you can:

#. Choose a site you want to install the add-on to from the dashboard.
#. Go to Apps > Install App
#. Click Install next to the FAQ app.
#. Redeploy the site.


*******************
Manual Installation
*******************


Requirements
============

- This project requires **django CMS 3.0.12** or later.


PIP dependency
==============

If you're installing into an existing django CMS project, you can run either::

    pip install aldryn-faq

or::

    pip install -e git+https://github.com/aldryn/aldryn-faq.git#egg=aldryn-faq

If you need to start a new project, we recommend that first you use the
`django CMS Installer <http://djangocms-installer.readthedocs.org>`_ to create
it, and then install Aldryn FAQ on top of that.


settings.py
===========

In your project's ``settings.py`` make sure you have all of::

    'adminsortable2',
    'aldryn_boilerplates',
    'aldryn_reversion',
    'aldryn_translation_tools',
    'djangocms_text_ckeditor',
    'parler',
    'sortedm2m',
    'aldryn_faq',
    'taggit',

listed in ``INSTALLED_APPS``, *after* ``'cms'``.


Additional Configuration
========================

.. important::

    To get Aldryn FAQ to work you need to add additional configurations:


1. Aldryn-Boilerplates
----------------------

You need set additional configurations to ``settings.py`` for `Aldryn
Boilerplates  <https://github.com/aldryn/aldryn-boilerplates#configuration>`_.

To use the old templates, set ``ALDRYN_BOILERPLATE_NAME='legacy'``.
To use https://github.com/aldryn/aldryn-boilerplate-bootstrap3 (recommended)
``set ALDRYN_BOILERPLATE_NAME='bootstrap3'``.


2. Django-Parler
----------------

If you plan to use translations, configure `django-parler
<https://pypi.python.org/pypi/django-parler/>`_.

Be sure to add ``PARLER_LANGUAGES`` to your settings with the appropriate
configuration for your project. Example: ::

    PARLER_LANGUAGES = {
       1: (
           {'code': 'en',},
           {'code': 'fr',},
           {'code': 'de',},
       ),
       'default': {
           'fallback': 'en',             # defaults to PARLER_DEFAULT_LANGUAGE_CODE
           'hide_untranslated': False,   # the default; let .active_translations() return fallbacks too.
       }
    }


Migrations
==========

Now run ``python manage.py migrate`` if you have not already done so,
followed by ``python manage.py migrate`` to prepare the database for the new
applications.

Now run ``python manage.py migrate aldryn_faq``.

.. note::

    Aldryn FAQ supports both South and Django 1.7 migrations.
    If using Django 1.6 and South < 1.0 you may need to add the following to
    your settings: ::

        SOUTH_MIGRATION_MODULES = {
           ...
           'taggit': 'taggit.south_migrations',
           'aldryn_faq': 'aldryn_faq.south_migrations',
           ...
        }


Server
======

To finish the setup, you need to create a page, change to the
*Advanced Settings* and choose *FAQ* within the *Application* drop-down.

You also need to set the *Application configurations* and
**publish the changes**.

Finally you just need to **restart your local development server** and you are
ready to go.

This process is described in more depth within :doc:`/how_to/basic_usage`.
