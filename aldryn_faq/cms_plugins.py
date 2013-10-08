# -*- coding: utf-8 -*-
from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_faq import models


class FAQPlugin(CMSPluginBase):

    module = "FAQ"


class LatestQuestionsPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/questions.html'
    name = _('Latest questions')
    model = models.LatestQuestionsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class TopQuestionsPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/questions.html'
    name = _('Top questions')
    model = models.TopQuestionsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class SelectedCategoryInline(TabularInline):
    model = models.SelectedCategory
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(SelectedCategoryInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'category':
            field.queryset = models.Category.objects.language()
        return field


class CategoryListPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/category_list.html'
    name = _('List of categories')
    model = models.CategoryListPlugin
    inlines = [SelectedCategoryInline]

    def render(self, context, instance, placeholder):
        context['categories'] = instance.get_categories()
        return context


plugin_pool.register_plugin(LatestQuestionsPlugin)
plugin_pool.register_plugin(TopQuestionsPlugin)
plugin_pool.register_plugin(CategoryListPlugin)
