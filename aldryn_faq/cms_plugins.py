# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_faq import models


class LatestQuestionsPlugin(CMSPluginBase):

    module = 'FAQ'
    render_template = 'aldryn_faq/plugins/latest_questions.html'
    name = _('Latest questions')
    model = models.LatestQuestionPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(LatestQuestionsPlugin)
