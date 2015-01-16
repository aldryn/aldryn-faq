# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.template import RequestContext

from cms.api import add_plugin

from aldryn_faq.models import SelectedCategory
from . import AldrynFaqTest, CMSRequestBasedTest


class TestQuestionListPlugin(AldrynFaqTest, CMSRequestBasedTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'QuestionListPlugin', language='en')

        # First test that it is initially empty
        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=False)
        context = RequestContext(request, {})
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find("<p>No entry found.</p>") > -1)

        # Now, add a question, and test that it renders.
        question1 = self.reload(self.question1, "en")
        plugin.questions.add(question1)
        plugin.save()
        request = self.get_page_request(
            page1, self.user, None, lang_code='en', edit=False)
        context = RequestContext(request, {})
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(question1.title) > -1)

        # Test its unicode method
        self.assertEqual(str(plugin), str(1))

        # Test its copy_relations. To do this, we'll create another instance
        # that is empty, then copy_relations to it, and prove that it contains
        # questions.
        plugin2 = add_plugin(ph, 'QuestionListPlugin', language='en')
        plugin2.copy_relations(plugin)
        self.assertTrue(plugin.get_questions(), plugin2.get_questions())


class TestLatestQuestionsPlugin(AldrynFaqTest, CMSRequestBasedTest):

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


class TestTopQuestionsPlugin(AldrynFaqTest, CMSRequestBasedTest):
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


class TestMostReadQuestionsPlugin(AldrynFaqTest, CMSRequestBasedTest):
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


class TestCategoryListPlugin(AldrynFaqTest, CMSRequestBasedTest):
    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'CategoryListPlugin', language='de')

        request = self.get_page_request(
            page1, self.user, None, lang_code='de', edit=False)
        context = RequestContext(request, {})
        url = self.reload(self.category1, "de").get_absolute_url()
        rendered = plugin.render_plugin(context, ph)
        # Why does this work? Probably because if there were no selected
        # categories, it returns all of them, and we only have 1 EN category?
        self.assertTrue(rendered.find(url) > -1)

        # Add some selected categories
        categories = [self.category1, self.category2]
        sc = None
        for idx, category in enumerate(categories):
            sc = SelectedCategory(
                category=category, position=idx, cms_plugin=plugin)
            sc.save()
        self.assertItemsEqual(plugin.get_categories(), categories)

        # While we're here, let's test that SelectedCategory's unicode works
        self.assertEqual(unicode(sc), categories[-1].name)

        # Test that copy_relations works
        plugin2 = add_plugin(ph, "CategoryListPlugin", language="de")
        plugin2.copy_relations(plugin)
        self.assertItemsEqual(
            plugin.get_categories(),
            plugin2.get_categories()
        )
