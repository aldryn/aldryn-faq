# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.utils import get_language_from_request
from adminsortable2.admin import SortableInlineAdminMixin

from . import models
from .forms import QuestionListPluginForm


class FAQPlugin(CMSPluginBase):

    module = "FAQ"


class QuestionListPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/question_list.html'
    name = _('Question List')
    model = models.QuestionListPlugin
    form = QuestionListPluginForm

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class LatestQuestionsPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/latest_questions.html'
    name = _('Latest questions')
    model = models.LatestQuestionsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class TopQuestionsPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/top_questions.html'
    name = _('Top questions')
    model = models.TopQuestionsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class MostReadQuestionsPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/most_read_questions.html'
    name = _('Most read questions')
    model = models.MostReadQuestionsPlugin
    cache = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


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
        return context


plugin_pool.register_plugin(CategoryListPlugin)
plugin_pool.register_plugin(LatestQuestionsPlugin)
plugin_pool.register_plugin(QuestionListPlugin)
plugin_pool.register_plugin(TopQuestionsPlugin)
plugin_pool.register_plugin(MostReadQuestionsPlugin)
