# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

from django.template import RequestContext
from django.utils.translation import override

from cms.api import add_plugin

from aldryn_faq.models import SelectedCategory
from .test_base import AldrynFaqTest

# NOTICE:
#
# For unknown reasons, in Django 1.8, this statement:
#
#     context = RequestContext(request, {})
#
# Seems to create a context that does not contain a request object, but only
# sometimes. This issue does not seem to exist in earlier versions of Django.
# Investigating further.
#
# The fix for now is to explicitly add another context item for the request
# object like so:
#
#     context = RequestContext(request, {"request": request})
#
# As required.


class TestQuestionListPlugin(AldrynFaqTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot="content")
        plugin = add_plugin(ph, "QuestionListPlugin", language="en")

        # First test that it is initially empty
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        context = RequestContext(request, {})
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find("No entry found.") > -1)

        # Now, add a question, and test that it renders.
        question1 = self.reload(self.question1, "en")
        plugin.questions.add(question1)
        plugin.save()
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        context = RequestContext(request, {"request": request})
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(question1.title) > -1)

        # Test its unicode method
        self.assertEqual(str(plugin), "1 question selected")

        # Test its copy_relations. To do this, we'll create another instance
        # that is empty, then copy_relations to it, and prove that it contains
        # questions.
        plugin2 = add_plugin(ph, "QuestionListPlugin", language="en")
        plugin2.copy_relations(plugin)
        self.assertTrue(plugin.get_questions(), plugin2.get_questions())


class TestLatestQuestionsPlugin(AldrynFaqTest):

    def test_plugin(self):
        with override("de"):
            page1 = self.get_or_create_page("Page One")
            ph = page1.placeholders.get(slot="content")
            plugin = add_plugin(ph, "LatestQuestionsPlugin", language="de")
            request = self.get_page_request(
                page1, self.user, None, lang_code="de", edit=False)
            context = RequestContext(request, {"request": request})
            url1 = self.reload(self.question1, "de").get_absolute_url()
            url2 = self.reload(self.question2, "de").get_absolute_url()
            rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(url1) > -1)
        self.assertTrue(rendered.find(url2) > -1)
        # Test that question2 appears before question1
        self.assertTrue(rendered.find(url2) < rendered.find(url1))


class TestTopQuestionsPlugin(AldrynFaqTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot="content")
        plugin = add_plugin(ph, "TopQuestionsPlugin", language="en")

        # First test that no plugins are found initially
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        context = RequestContext(request, {})
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find("No entry found") > -1)

        # Now test, set a question to be "top", then test that it appears.
        self.question1.is_top = True
        self.question1.save()
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        context = RequestContext(request, {"request": request})
        question1 = self.reload(self.question1, "en")
        rendered = plugin.render_plugin(context, ph)
        self.assertTrue(rendered.find(question1.title) > -1)


class TestMostReadQuestionsPlugin(AldrynFaqTest):
    def test_plugin(self):
        # Prepare the questions...
        self.question1.number_of_visits = 5
        self.question1.save()
        self.question2.number_of_visits = 10
        self.question2.save()

        with override("de"):
            page1 = self.get_or_create_page("Page One")
            ph = page1.placeholders.get(slot="content")
            plugin = add_plugin(ph, "MostReadQuestionsPlugin", language="de")
            request = self.get_page_request(
                page1, self.user, None, lang_code="de", edit=False)
            context = RequestContext(request, {"request": request})
            url1 = self.reload(self.question1, "de").get_absolute_url()
            url2 = self.reload(self.question2, "de").get_absolute_url()
            rendered = plugin.render_plugin(context, ph)
        # Ensure both questions appear...
        self.assertTrue(rendered.find(url1) > -1)
        self.assertTrue(rendered.find(url2) > -1)
        # Test that question2 appears before question1
        self.assertTrue(rendered.find(url2) < rendered.find(url1))


class TestCategoryListPlugin(AldrynFaqTest):
    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot='content')
        plugin = add_plugin(ph, 'CategoryListPlugin', language="de")

        request = self.get_page_request(
            page1, self.user, None, lang_code="de", edit=False)
        context = RequestContext(request, {})
        category1 = self.category1
        category1.save()
        category2 = self.category2
        category2.save()
        url = category1.get_absolute_url(language="de")
        rendered = plugin.render_plugin(context, ph)
        self.assertFalse(rendered.find(url) > -1)

        # Add some selected categories
        categories = [self.category1, self.category2]
        sc = None
        for idx, category in enumerate(categories):
            sc = SelectedCategory(
                category=category, position=idx, cms_plugin=plugin)
            sc.save()
        self.assertEqualItems(
            [c.id for c in plugin.get_categories()],
            [c.id for c in categories]
        )

        # While we're here, let's test that SelectedCategory's __str__ works
        if six.PY2:
            self.assertEqual(unicode(sc), categories[-1].name)
        else:
            self.assertEqual(str(sc), categories[-1].name)

        # Test that copy_relations works
        plugin2 = add_plugin(ph, "CategoryListPlugin", language="de")
        plugin2.copy_relations(plugin)
        self.assertEqualItems(
            [c.id for c in plugin.get_categories()],
            [c.id for c in plugin2.get_categories()]
        )
