CHANGELOG
=========

1.0.3 (2015-08-06)
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
