# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from distutils.version import LooseVersion

from django.contrib import admin
from django.templatetags.static import static
from django.utils.translation import ugettext as _
from django.utils.html import escape

import cms
from cms.admin.placeholderadmin import FrontendEditableAdminMixin

from adminsortable2.admin import SortableAdminMixin
from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_reversion.admin import VersionedPlaceholderAdminMixin
from aldryn_translation_tools.admin import AllTranslationsMixin
from parler.admin import TranslatableAdmin

from .models import Category, Question, FaqConfig
from .forms import CategoryAdminForm


class CategoryAdmin(AllTranslationsMixin,
                    VersionedPlaceholderAdminMixin,
                    TranslatableAdmin):

    list_display = ('__str__', 'appconfig', )

    form = CategoryAdminForm

    _fieldsets = [
        (None, {
            'fields': ('name', 'slug', )
        }),
        (_('Language Independent Fields'), {
            'fields': ('appconfig', )
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('description',)
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


class QuestionAdmin(AllTranslationsMixin,
                    VersionedPlaceholderAdminMixin,
                    FrontendEditableAdminMixin,
                    SortableAdminMixin,
                    TranslatableAdmin):

    render_placeholder_language_tabs = False
    list_display = [
        '__str__', 'category', 'tag_list', 'is_top', 'number_of_visits']
    list_filter = ['category', 'translations__language_code']
    frontend_editable_fields = ('title', 'category', 'answer_text')
    readonly_fields = ['number_of_visits']

    def tag_list(self, obj):
        """
        Displays Taggit tags to a comma-separated list of the tags’ names.
        """
        escaped_tags = [escape(tag.name) for tag in obj.tags.get_query_set()]
        return ", ".join(escaped_tags)
    tag_list.short_description = 'Tags'
    tag_list.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': [
                    'title', 'slug', 'category', 'answer_text', 'tags',
                    'is_top', 'number_of_visits']
            })
        ]
        cms_compat_fieldset = {
            'classes': ['plugin-holder', 'plugin-holder-nopage'],
            'fields': ['answer']
        }

        # show placeholder field if not CMS 3.0
        if LooseVersion(cms.__version__) < LooseVersion('3.0'):
            fieldsets.append(('Short description', cms_compat_fieldset))
        return fieldsets


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)


class FaqConfigAdmin(AllTranslationsMixin,
                     VersionedPlaceholderAdminMixin,
                     BaseAppHookConfig,
                     TranslatableAdmin):
    def get_config_fields(self):
        return (
            'app_title',
            'permalink_type', 'non_permalink_handling',
            'config.show_description',
        )

admin.site.register(FaqConfig, FaqConfigAdmin)
