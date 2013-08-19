# -*- coding: utf-8 -*-
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


class CategoryListPlugin(FAQPlugin):

    render_template = 'aldryn_faq/plugins/category_list.html'
    name = _('List of categories')
    model = CMSPlugin

    def render(self, context, instance, placeholder):
        context['categories'] = (models.Category.objects
                                 .get_categories(instance.language))
        return context


plugin_pool.register_plugin(LatestQuestionsPlugin)
plugin_pool.register_plugin(TopQuestionsPlugin)
plugin_pool.register_plugin(CategoryListPlugin)
