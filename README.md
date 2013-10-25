Aldryn FAQ App
===============

Simple faq application. It allows you to:

- write a questions and answers


Installation
============

Aldryn Platrofm Users
---------------------

Choose a site you want to install the add-on to from the dashboard. Then go to ``Apps -> Install app`` and click ``Install`` next to ``FAQ`` app.

Redeploy the site.

Manuall Installation
--------------------

Run ``pip install aldryn-faq``.

Add below apps to ``INSTALLED_APPS``:

    INSTALLED_APPS = [
        …
        
        'aldryn_faq',
        'djangocms_text_ckeditor',
        'adminsortable',
        'django-sortedm2m',
        'hvad',
        …
    ]

Listing
=======

You can add question/answer in the admin interface now. Search for the label ``Aldryn_Faq``.

In order to display them, create a CMS page and install the app there (choose ``FAQ`` from the ``Advanced Settings -> Application`` dropdown).

Now redeploy/restart the site again.

The above CMS site has become a faq list view.

