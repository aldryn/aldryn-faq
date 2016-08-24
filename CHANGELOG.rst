CHANGELOG
=========

1.2.2 (UNRELEASED)
------------------

* Fixed related_name inconsistency with django CMS 3.3.1
* Dropped support for djangoCMS < 3.2
* Introduced support for djangoCMS 3.4.0


1.2.1 (2016-06-28)
------------------

* Added support for cache durations fields in "time-sensitive" plugins on django CMS 3.3.0+
* Updated translations


1.2.0 (2016-06-09)
------------------

* Compatibility for Py35, Dj19, and CMS33 combinations
* Improved frontend testing


1.1.1 (2016-05-20)
------------------

* Update test matrices for Py35, Dj19, and CMS33 combinations


1.1.0 (2016-03-10)
------------------

* Add stripped default django templates to `/aldryn_faq/templates`
* Remove unused render_placeholder configs
* Add static_placeholders where necessary
* Simplify templates


1.0.13 (2016-02-25)
-------------------

* Fixes error if tags were filled with non-ascii characters.
* Added an optional description field to category.


1.0.12 (2016-02-12)
-------------------

* Add Django 1.9 support.
* Clean up test environments.
* Add default FaqConfig migrations.


1.0.11 (2016-01-12)
-------------------

* Adjust requirements for django-reversion to allow 1.10


1.0.10 (2016-01-12)
-------------------

* Improves support for current versions of django-reversion
* Adds FE tests against DMS 3.2


1.0.9 (2016-01-09)
------------------

* Adds reversion support to wizards
* Updates test configuration


1.0.8 (2015-12-01)
------------------

* Fixes issue with toolbar (when language is different than the page language)
* Fixes issue for plugins if category didn't had a valid namespace
* Fixes Attribute error on menu processing


1.0.7 (2015-11-12)
------------------

* Wizards for CMS 3.2
* Fix issue when updating form <1.0.6 to 1.0.7+ (slug generation for questions)
  **Note** that 1.0.6 is still affected.


1.0.6 (2015-09-04)
------------------

* Support for Django 1.8
* Updated requirements
* More reversion support
* Added permalink options and support


1.0.5 (2015-08-07)
------------------

* Improvements to FAQ CMSToolbar


1.0.4 (2015-08-06)
------------------

* Documentation improvements
* Pins Aldryn Translation Tools to >=0.1.0
* Pins Aldryn Reversion to >=0.1.0
* Pins Aldryn Boilerplates to >=0.6.0
* Improvements to FAQ CMSToolbar


1.0.3 (2015-07-22)
------------------

* Unrestrict Aldryn Translation Tools version.

1.0.2 (2015-07-22)
------------------

* Much better handling of language fallbacks
* Add automated frontend tests and configuration
* Improved admin display of translations
* Fix up some dependencies

0.13.0 (2015-06-26)
-------------------

* README cleanups
* Adds documentation
* Categories in the CategoryList plugin are now re-arrangeable via drag-and-drop
  as opposed to manually managing a sort metric.
* The Category List view and the Question List pages in different apphooks can
  now be presented differently if so required via new Placeholder Fields.
* The older, Static Placeholders still remain for this release, but are marked
  in the mark-up as "DEPRECATED". Please use this release to migrate any plugins
  in these plugins to their respective PlaceholderField replacements. These will
  be remove in the next release.

0.12.6 (2015-04-16)
-------------------

* Use get_current_language from cms instead get_language from Django because Django bug #9340

0.12.0 (2015-03-25)
-------------------

* Adds reversion support
* Switch to django-admin-sortable2 v0.5.0 or later

0.11.0 (2015-02-03)
-------------------

* multi-boilerplate support
  new requirement: aldryn-boilerplates (needs configuration)
* added bootstrap templates
