# -*- coding: utf-8 -*-
from distutils.version import LooseVersion

from django.contrib import admin
from django.templatetags.static import static

import cms
from cms.admin.placeholderadmin import PlaceholderAdmin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin

from adminsortable.admin import SortableAdmin

from hvad.admin import TranslatableAdmin

from .models import Category, Question
from .forms import CategoryAdminForm


class CategoryAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'all_translations']

    form = CategoryAdminForm

    _fieldsets = [(None, {'fields': ['name', 'slug']})]

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


class QuestionAdmin(FrontendEditableAdminMixin, SortableAdmin,
                    PlaceholderAdmin, TranslatableAdmin):

    render_placeholder_language_tabs = False
    list_display = ['__unicode__', 'category', 'is_top', 'number_of_visits']
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
