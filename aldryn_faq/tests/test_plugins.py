# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.template import RequestContext
from cms.api import add_plugin
from aldryn_faq.models import Question  # , Category, get_slug_in_language

# from cms.utils.i18n import force_language
# from hvad.test_utils.context_managers import LanguageOverride

from . import AldrynFaqTest, CMSRequestBasedTest


class TestQuestionListPlugin(AldrynFaqTest, CMSRequestBasedTest):

    # def test_plugin(self):
    #     page1 = self.get_or_create_page("Page One")
    #     ph = page1.placeholders.get(slot='content')
    #     plugin = add_plugin(ph, 'QuestionListPlugin', language='en')

    #     request = self.get_page_request(
    #         page1, self.user, None, lang_code='en', edit=True)
    #     context = RequestContext(request, {})
    #     question1 = self.reload(self.question1, "en")
    #     rendered = plugin.render_plugin(context, ph)
    #     self.assertTrue(rendered.find(question1.title) > -1)
    pass


class TestCategoryListPlugin(AldrynFaqTest, CMSRequestBasedTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'CategoryListPlugin', language='en')

        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=True)
        context = RequestContext(request, {})
        url = self.reload(self.category1, "en").get_absolute_url()
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(url) > -1)
