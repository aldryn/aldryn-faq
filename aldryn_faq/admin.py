# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from distutils.version import LooseVersion

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.templatetags.static import static
from django.utils.translation import get_language, ugettext as _

import cms
from cms.admin.placeholderadmin import FrontendEditableAdminMixin

from adminsortable2.admin import SortableAdminMixin
from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_reversion.admin import VersionedPlaceholderAdminMixin
from parler.admin import TranslatableAdmin
# from reversion import VersionAdminm

from .models import Category, Question, FaqConfig
from .forms import CategoryAdminForm


class AllTranslationsAdminMixin(object):
    """To use this, apply this mixin to your Admin class, then add
    'all_translations' to your list_display list."""

    def all_translations(self, obj):
        """This is an adapter for the functionality that was in HVAD."""
        available = list(obj.get_available_languages())
        langs = []
        for lang, _language_name in settings.LANGUAGES:
            if lang in available:
                langs.append(lang)
                available.remove(lang)
        langs += available
        for idx, lang in enumerate(langs):
            change_form_url = reverse('admin:{app_label}_{model_name}_change'.format(
                app_label=obj._meta.app_label.lower(),
                model_name=obj.__class__.__name__.lower(),
            ), args=(obj.id, ))
            link = '<a href="{url}?language={lang}">{lang}</a>'.format(
                url=change_form_url,
                lang=lang,
            )
            if lang == get_language():
                link = "<strong>{0}</strong>".format(link)
            langs[idx] = link
        return ', '.join(langs)
    all_translations.short_description = 'available translations'
    all_translations.allow_tags = True


class CategoryAdmin(AllTranslationsAdminMixin, TranslatableAdmin):

    list_display = ('__str__', 'all_translations', 'appconfig', )

    form = CategoryAdminForm

    _fieldsets = [
        (None, {
            'fields': ('name', 'slug', )
        }),
        (_('Language Independent Fields'), {
            'fields': ('appconfig', )
        }),
    ]

    class Media:
        # Django BUG - Django only checks for self.prepopulated_fields to
        # determine if it should include these files. But it never checks
        # get_prepopulated_fields()
        js = [static('admin/js/%s' % url) for url in (
            'urlify.js', 'prepopulate.min.js')]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ['name']}

    def get_fieldsets(self, request, obj=None):
        return self._fieldsets


class QuestionAdmin(VersionedPlaceholderAdminMixin,
                    FrontendEditableAdminMixin,
                    SortableAdminMixin, TranslatableAdmin):

    render_placeholder_language_tabs = False
    list_display = ['__str__', 'category', 'is_top', 'number_of_visits']
    list_filter = ['category', 'translations__language_code']
    frontend_editable_fields = ('title', 'category', 'answer_text')
    readonly_fields = ['number_of_visits']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': [
                    'title', 'category', 'answer_text', 'is_top',
                    'number_of_visits']
            })
        ]
        cms_compat_fieldset = {
            'classes': ['plugin-holder', 'plugin-holder-nopage'],
            'fields': ['answer']
        }

        # show placeholder field if not CMS 3.0
        if LooseVersion(cms.__version__) < LooseVersion('3.0'):
            fieldsets.append(('Answer', cms_compat_fieldset))
        return fieldsets


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)


class FaqConfigAdmin(TranslatableAdmin, BaseAppHookConfig):
    def get_config_fields(self):
        return ('app_title', )

admin.site.register(FaqConfig, FaqConfigAdmin)
