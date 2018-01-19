# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from distutils.version import LooseVersion

import six

from django.template import RequestContext
from django.utils.translation import override
import cms
from cms.api import add_plugin

from ..models import SelectedCategory
from .test_base import AldrynFaqTest


def _render_plugin(request, plugin):
    def _render_via_django():
        from django.template import Engine
        context = RequestContext(request)
        updates = {}
        engine = Engine.get_default()

        for processor in engine.template_context_processors:
            updates.update(processor(context.request))
        context.dicts[context._processors_index] = updates

        return plugin.render_plugin(context)

    def _render_via_cms():
        from cms.plugin_rendering import ContentRenderer
        renderer = ContentRenderer(request)
        context = RequestContext(request)
        # Avoid errors if plugin require a request object
        # when rendering.
        context['request'] = request
        return renderer.render_plugin(plugin, context)

    cms_lt_3_4 = LooseVersion(cms.__version__) < LooseVersion('3.4')  # COMPAT: CMS3.4
    if cms_lt_3_4:
        return _render_via_django()
    else:
        return _render_via_cms()


class TestQuestionListPlugin(AldrynFaqTest):

    def test_plugin(self):
        page1 = self.get_or_create_page("Page One")
        ph = page1.placeholders.get(slot="content")
        plugin = add_plugin(ph, "QuestionListPlugin", language="en")

        # First test that it is initially empty
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        rendered = _render_plugin(request, plugin)
        self.assertTrue(rendered.find("No entry found.") > -1)

        # Now, add a question, and test that it renders.
        question1 = self.reload(self.question1, "en")
        plugin.questions.add(question1)
        plugin.save()
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        rendered = _render_plugin(request, plugin)
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
            url1 = self.reload(self.question1, "de").get_absolute_url()
            url2 = self.reload(self.question2, "de").get_absolute_url()
            rendered = _render_plugin(request, plugin)
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
        rendered = _render_plugin(request, plugin)
        self.assertTrue(rendered.find("No entry found") > -1)

        # Now test, set a question to be "top", then test that it appears.
        self.question1.is_top = True
        self.question1.save()
        request = self.get_page_request(
            page1, self.user, None, lang_code="en", edit=False)
        question1 = self.reload(self.question1, "en")
        rendered = _render_plugin(request, plugin)
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
            url1 = self.reload(self.question1, "de").get_absolute_url()
            url2 = self.reload(self.question2, "de").get_absolute_url()
            rendered = _render_plugin(request, plugin)
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
        category1 = self.category1
        category1.save()
        category2 = self.category2
        category2.save()
        url = category1.get_absolute_url(language="de")
        rendered = _render_plugin(request, plugin)
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
