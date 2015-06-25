##########
ALDRYN FAQ
##########

It is written to support full internationalization; questions and their answers
can be managed in multiple lanauges.

Aldryn FAQ supports "spaces" (apphook_config-able) so that multiple, independent
instances of this app can be attached to multiple pages in the same project, if
necessary.

It is also written to support Django Reversion which allows content managers to
roll-back to previous edits should this be necessary.


Installation & Usage
--------------------

Aldryn Platform Users
~~~~~~~~~~~~~~~~~~~~~

1) Choose a site you want to install the add-on to from the dashboard.

2) Go to **Apps** -> **Install App**

3) Click **Install** next to **FAQ** app.

4) Redeploy the site.


Manual Installation
~~~~~~~~~~~~~~~~~~~

1) Run ``pip install aldryn-faq``.

2) Add below apps to ``INSTALLED_APPS``: ::

       INSTALLED_APPS = [
           …
           'adminsortable2',
           'aldryn_reversion',
           'djangocms_text_ckeditor',
           'parler',
           'sortedm2m',
           'aldryn_faq',
           …
       ]

3) Configure ``aldryn-boilerplates`` (https://pypi.python.org/pypi/aldryn-boilerplates/).

   To use the old templates, set ``ALDRYN_BOILERPLATE_NAME='legacy'``.
   To use https://github.com/aldryn/aldryn-boilerplate-standard (recommended, will be renamed to
   ``aldryn-boilerplate-bootstrap3``) set ``ALDRYN_BOILERPLATE_NAME='bootstrap3'``.

4) If you plan to use translations, configure ``django-parler`` (https://pypi.python.org/pypi/django-parler/)

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

5) Run migrations: `python manage.py migrate aldryn_faq`.

   NOTE: aldryn_faq supports both South and Django 1.7 migrations. However, if
   your project uses a version of South older than 1.0.3, you may need to add
   the following to your settings: ::

      MIGRATION_MODULES = {
          # ...
          'aldryn_faq': 'aldryn_faq.migrations_django',
          # ...
      },

6) (Re-)Start your application server.


Listing
~~~~~~~

You can add question/answer in the admin interface now. Search for the label
``Aldryn_Faq``.

In order to display them, create a CMS page and install the app there (choose
``FAQ`` from the ``Advanced Settings -> Application`` dropdown).

Now redeploy/restart the site again.

The above CMS page has become a faq list view.


NOTES
-----

django-admin-sortable2
~~~~~~~~~~~~~~~~~~~~~~

This project uses django-admin-sortable2 version 0.5.0 or later. Installing an
earlier version of django-admin-sortable2 will cause migrations to fail due to a
package name clash with django-admin-sortable.
