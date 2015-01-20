# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils.translation import override

from aldryn_faq.models import Category, Question, get_slug_in_language

from . import AldrynFaqTest


class TestCategory(AldrynFaqTest):

    def test_unicode(self):
        with override('en'):
            category1 = self.reload(self.category1)
            self.assertEqual(
                force_text(category1), self.data["category1"]["en"]["name"])
        with override('de'):
            category1 = self.reload(self.category1)
            self.assertEqual(
                force_text(category1), self.data["category1"]["de"]["name"])

    def test_get_slug_in_language(self):
        self.assertIsNone(get_slug_in_language(None, 'en'), None)
        self.assertIsNone(get_slug_in_language(object, 'en'), None)
        self.assertEqual(
            get_slug_in_language(self.category1, 'en'),
            self.data["category1"]["en"]["slug"]
        )
        self.assertEqual(
            get_slug_in_language(self.category1, 'de'),
            self.data["category1"]["de"]["slug"]
        )
        # Test non-existent translation
        self.assertEqual(
            get_slug_in_language(self.category1, 'qq'),
            None
        )

    def test_model_type_id(self):
        ct = ContentType.objects.get(app_label='aldryn_faq', model='category')
        self.assertEqual(
            self.category1.model_type_id(),
            ct.id
        )

    def test_get_absolue_url(self):
        self.assertEqual(
            self.category1.get_absolute_url("en"),
            "/en/faq/example/"
        )
        self.assertEqual(
            self.category1.get_absolute_url("de"),
            "/de/faq/beispiel/"
        )

    def test_manager_get_categories(self):
        # Test case when no language is passed. Apparently, this returns only
        # those objects that have the default language translations.
        # TODO: Verify that this is the intended behavior.
        # self.assertEqualItems(
        #     [c.id for c in Category.objects.get_categories()],
        #     [self.category1.id, ]
        # )

        # Test case of requesting objects of only a single language. In our
        # setup, we have 1 category in EN and 2 in DE.
        categories = Category.objects.get_categories('en')
        self.assertEqualItems(
            [category.id for category in categories],
            [self.category1.id, ]
        )

        # There's actually two categories in DE
        categories = Category.objects.get_categories('de')
        cids = set([category.id for category in categories])
        self.assertEqual(
            cids,
            set([self.category1.id, self.category2.id])
        )


class TestQuestion(AldrynFaqTest):

    def test_unicode(self):
        with override('en'):
            question1 = self.reload(self.question1)
            self.assertEqual(
                force_text(question1),
                self.data["question1"]["en"]["title"]
            )
        with override('de'):
            question1 = self.reload(self.question1)
            self.assertEqual(
                force_text(question1),
                self.data["question1"]["de"]["title"]
            )

    def test_model_type_id(self):
        ct = ContentType.objects.get(app_label='aldryn_faq', model='question')
        self.assertEqual(
            self.question1.model_type_id(),
            ct.id
        )

    def test_get_absolue_url(self):
        self.assertEqual(
            self.question1.get_absolute_url("en"),
            "/en/faq/example/1/"
        )
        self.assertEqual(
            self.question1.get_absolute_url("de"),
            "/de/faq/beispiel/1/"
        )

    def test_manager_filter_by_language(self):
        questions = Question.objects.filter_by_language('en')
        self.assertEqualItems(
            [q.id for q in questions],
            [self.question1.id]
        )

        questions = Question.objects.filter_by_language('de')
        self.assertEqualItems(
            [q.id for q in questions],
            [self.question1.id, self.question2.id]
        )

    def test_manager_filter_by_current_language(self):
        with override("en"):
            questions = Question.objects.filter_by_current_language()
            self.assertEqualItems(
                [q.id for q in questions],
                [self.question1.id]
            )

        with override("de"):
            questions = Question.objects.filter_by_current_language()
            self.assertEqualItems(
                [q.id for q in questions],
                [self.question1.id, self.question2.id]
            )


class TestFAQTranslations(AldrynFaqTest):

    def test_fetch_faq_translations(self):
        """Test we can fetch arbitrary translations of the question and
        its category."""
        # Can we target the EN values?
        with override("en"):
            question1 = self.reload(self.question1)
            category1 = self.reload(self.question1.category)
            self.assertEqual(
                question1.title,
                self.data["question1"]["en"]["title"]
            )
            self.assertEqual(
                question1.answer_text,
                self.data["question1"]["en"]["answer_text"]
            )
            self.assertEqual(
                category1.name,
                self.data["category1"]["en"]["name"]
            )
            self.assertEqual(
                category1.slug,
                self.data["category1"]["en"]["slug"]
            )

        # And the DE values?
        with override("de"):
            question1 = self.reload(self.question1)
            category1 = self.reload(self.question1.category)
            self.assertEqual(
                question1.title,
                self.data["question1"]["de"]["title"]
            )
            self.assertEqual(
                question1.answer_text,
                self.data["question1"]["de"]["answer_text"]
            )
            self.assertEqual(
                category1.name,
                self.data["category1"]["de"]["name"]
            )
            self.assertEqual(
                category1.slug,
                self.data["category1"]["de"]["slug"]
            )
