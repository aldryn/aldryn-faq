# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.template import RequestContext
from cms.api import add_plugin

# from cms.utils.i18n import force_language
# from hvad.test_utils.context_managers import LanguageOverride
# from aldryn_faq.models import Category, Question, get_slug_in_language

from . import AldrynFaqTest, CMSRequestBasedTest


class TestQuestionListPlugin(AldrynFaqTest, CMSRequestBasedTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'QuestionListPlugin', language='en')

        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=True)
        context = RequestContext(request, {})
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(self.question1.title) > -1)


class TestCategoryListPlugin(AldrynFaqTest, CMSRequestBasedTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'CategoryListPlugin', language='en')

        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=True)
        context = RequestContext(request, {})
        try:
            rendered = plugin.render_plugin(context, ph)
            self.assertTrue(rendered.find(self.category1.name) > -1)
        except Exception as e:
            self.fail(e)
