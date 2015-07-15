# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from distutils.version import LooseVersion

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.templatetags.static import static
from django.utils.translation import ugettext as _

import cms
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from cms.utils.i18n import get_current_language

from adminsortable2.admin import SortableAdminMixin
from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_reversion.admin import VersionedPlaceholderAdminMixin
from aldryn_translation_tools.admin import AllTranslationsMixin
from parler.admin import TranslatableAdmin

from .models import Category, Question, FaqConfig
from .forms import CategoryAdminForm


class CategoryAdmin(AllTranslationsMixin, TranslatableAdmin):

    list_display = ('__str__', 'appconfig', )

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
        # Workaround for known Django bug: #24467
        # https://code.djangoproject.com/ticket/24467
        # Django checks for self.prepopulated_fields to determine if it should
        # include populate.js. But it never checks get_prepopulated_fields().
        # Fix is slated for Django 1.9 release, so this needs to remain until
        # we no longer support Django 1.8 or lower.
        js = [static('admin/js/%s' % url) for url in (
            'urlify.js', 'prepopulate.min.js')]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ['name']}

    def get_fieldsets(self, request, obj=None):
        return self._fieldsets


class QuestionAdmin(VersionedPlaceholderAdminMixin,
                    FrontendEditableAdminMixin,
                    SortableAdminMixin,
                    AllTranslationsMixin,
                    TranslatableAdmin):

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


class FaqConfigAdmin(AllTranslationsMixin,
                     BaseAppHookConfig,
                     TranslatableAdmin):
    def get_config_fields(self):
        return ('app_title', )

admin.site.register(FaqConfig, FaqConfigAdmin)
