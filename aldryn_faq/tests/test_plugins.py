# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.template import RequestContext
from cms.api import add_plugin
from aldryn_faq.models import Question  # , Category, get_slug_in_language

# from cms.utils.i18n import force_language
# from hvad.test_utils.context_managers import LanguageOverride

from . import AldrynFaqTest, CMSRequestBasedTest


class PluginBaseTest(AldrynFaqTest, CMSRequestBasedTest):
    def setUp(self):
        super(PluginBaseTest, self).setUp()
        pass


class TestQuestionListPlugin(PluginBaseTest):
    # TODO, this plugin doesn't appear to work!
    pass
    # def test_plugin(self):
    #     page1 = self.get_or_create_page("Page One")
    #     ph = page1.placeholders.get(slot='content')
    #     plugin = add_plugin(ph, 'QuestionListPlugin', language='en')

    #     request = self.get_page_request(
    #         page1, self.user, None, lang_code='en', edit=False)
    #     context = RequestContext(request, {})
    #     question1 = self.reload(self.question1, "en")
    #     rendered = plugin.render_plugin(context, ph)
    #     self.assertTrue(rendered.find(question1.title) > -1)


class TestLatestQuestionsPlugin(PluginBaseTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot="content")
        plugin = add_plugin(ph, "LatestQuestionsPlugin", language="en")
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        context = RequestContext(request, {})
        url1 = self.reload(self.question1, "en").get_absolute_url()
        url2 = self.reload(self.question2, "en").get_absolute_url()
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(url1) > -1)
        self.assertTrue(rendered.find(url2) > -1)
        # Test that question2 appears before question1
        self.assertTrue(rendered.find(url2) < rendered.find(url1))


class TestTopQuestionsPlugin(PluginBaseTest):
    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'TopQuestionsPlugin', language='en')

        # First test that no plugins are found initially
        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=False)
        context = RequestContext(request, {})
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find("No entry found") > -1)

        # Now test, set a question to be "top", then test that it appears.
        self.question1.is_top = True
        self.question1.save()
        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=False)
        context = RequestContext(request, {})
        question1 = self.reload(self.question1, "en")
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(question1.title) > -1)


class TestMostReadQuestionsPlugin(PluginBaseTest):
    def test_plugin(self):
        # Prepare the questions...
        self.question1.number_of_visits = 5
        self.question1.save()
        self.question2.number_of_visits = 10
        self.question2.save()

        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot="content")
        plugin = add_plugin(ph, "MostReadQuestionsPlugin", language="en")
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        context = RequestContext(request, {})
        url1 = self.reload(self.question1, "en").get_absolute_url()
        url2 = self.reload(self.question2, "en").get_absolute_url()
        rendered = plugin.render_plugin(context, ph)
        # Ensure both questions appear...
        self.assertTrue(rendered.find(url1) > -1)
        self.assertTrue(rendered.find(url2) > -1)
        # Test that question2 appears before question1
        self.assertTrue(rendered.find(url2) < rendered.find(url1))


class TestCategoryListPlugin(PluginBaseTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'CategoryListPlugin', language='en')

        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=False)
        context = RequestContext(request, {})
        url = self.reload(self.category1, "en").get_absolute_url()
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(url) > -1)
