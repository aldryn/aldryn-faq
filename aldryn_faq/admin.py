# -*- coding: utf-8 -*-
from adminsortable.admin import SortableAdmin
from cms.admin.placeholderadmin import PlaceholderAdmin
from django.contrib import admin
from distutils.version import LooseVersion
from hvad.admin import TranslatableAdmin

import cms

from . import models
from aldryn_faq.forms import CategoryForm
from cms.admin.placeholderadmin import FrontendEditableAdminMixin


class CategoryAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'all_translations']
    form = CategoryForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets


class QuestionAdmin(FrontendEditableAdminMixin, SortableAdmin, PlaceholderAdmin, TranslatableAdmin):

    render_placeholder_language_tabs = False
    list_display = ['__unicode__', 'category', 'is_top', 'number_of_visits']
    list_filter = ['category', 'translations__language_code']
    frontend_editable_fields = ('title', 'category', 'answer_text'),
    readonly_fields = ['number_of_visits']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': ['title', 'category', 'answer_text', 'is_top', 'number_of_visits']
            })
        ]

        # show placeholder field if not CMS 3.0
        if LooseVersion(cms.__version__) < LooseVersion('3.0'):
            fieldsets.append(
                ('Answer', {
                    'classes': ['plugin-holder', 'plugin-holder-nopage'],
                    'fields': ['answer']
                }))

        return fieldsets

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Category, CategoryAdmin)
