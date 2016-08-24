# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from distutils.version import LooseVersion
from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _

from cms import __version__ as cms_version
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.utils import get_language_from_request
from adminsortable2.admin import SortableInlineAdminMixin

from . import models
from .forms import QuestionListPluginForm

CMS_GTE_330 = LooseVersion(cms_version) >= LooseVersion('3.3.0')


class FAQPlugin(CMSPluginBase):

    module = "FAQ"


class AdjustableCacheMixin(object):
    """
    For django CMS < 3.3.0 installations, we have no choice but to disable the
    cache where there is time-sensitive information. However, in later CMS
    versions, we can configure it with `get_cache_expiration()`.
    """
    if not CMS_GTE_330:
        cache = False

    def get_cache_expiration(self, request, instance, placeholder):
        return getattr(instance, 'cache_duration', 0)

    def get_fieldsets(self, request, obj=None):
        """
        Removes the cache_duration field from the displayed form if we're not
        using django CMS v3.3.0 or later.
        """
        fieldsets = super(AdjustableCacheMixin, self).get_fieldsets(
            request, obj=None)
        if CMS_GTE_330:
            return fieldsets

        field = 'cache_duration'
        for fieldset in fieldsets:
            new_fieldset = [
                item for item in fieldset[1]['fields'] if item != field]
            fieldset[1]['fields'] = tuple(new_fieldset)
        return fieldsets


class QuestionListPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/question_list.html'
    name = _('Question List')
    model = models.QuestionListPlugin
    form = QuestionListPluginForm


class LatestQuestionsPlugin(AdjustableCacheMixin, FAQPlugin):

    render_template = 'aldryn_faq/plugins/latest_questions.html'
    name = _('Latest questions')
    model = models.LatestQuestionsPlugin


class TopQuestionsPlugin(AdjustableCacheMixin, FAQPlugin):

    render_template = 'aldryn_faq/plugins/top_questions.html'
    name = _('Top questions')
    model = models.TopQuestionsPlugin


class MostReadQuestionsPlugin(AdjustableCacheMixin, FAQPlugin):

    render_template = 'aldryn_faq/plugins/most_read_questions.html'
    name = _('Most read questions')
    model = models.MostReadQuestionsPlugin


class SelectedCategoryInline(SortableInlineAdminMixin, TabularInline):
    model = models.SelectedCategory
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(SelectedCategoryInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

        if db_field.name == 'category':
            language = get_language_from_request(request)
            field.queryset = models.Category.objects.language(language)
        return field


class CategoryListPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/category_list.html'
    name = _('List of categories')
    model = models.CategoryListPlugin
    inlines = [SelectedCategoryInline]

    def render(self, context, instance, placeholder):
        context['categories'] = instance.get_categories()
        return super(CategoryListPlugin, self).render(
            context, instance, placeholder)


plugin_pool.register_plugin(CategoryListPlugin)
plugin_pool.register_plugin(LatestQuestionsPlugin)
plugin_pool.register_plugin(QuestionListPlugin)
plugin_pool.register_plugin(TopQuestionsPlugin)
plugin_pool.register_plugin(MostReadQuestionsPlugin)
