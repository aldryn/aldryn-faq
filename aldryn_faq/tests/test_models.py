# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.utils.translation import override

from aldryn_faq.models import Category, Question, get_slug_in_language

from .test_base import AldrynFaqTest


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

    def test_model_type_id(self):
        ct = ContentType.objects.get(app_label='aldryn_faq', model='category')
        self.assertEqual(
            self.category1.model_type_id(),
            ct.pk
        )

    def test_get_absolute_url(self):
        category_1 = self.category1

        self.assertEqual(
            category_1.get_absolute_url("en"),
            "/en/faq/1-example/"
        )
        self.assertEqual(
            category_1.get_absolute_url("de"),
            "/de/faq/1-beispiel/"
        )

    def test_manager_get_categories(self):
        # Test case when no language is passed. Apparently, this returns only
        # those objects that have the default language translations.
        # TODO: Verify that this is the intended behavior.
        # self.assertEqualItems(
        #     [c.pk for c in Category.objects.get_categories()],
        #     [self.category1.pk, ]
        # )

        # Test case of requesting objects of only a single language. In our
        # setup, we have 1 category in EN and 2 in DE.
        categories = Category.objects.get_categories('en')
        self.assertEqualItems(
            [category.pk for category in categories],
            [self.category1.pk, ]
        )

        # There's actually two categories in DE
        categories = Category.objects.get_categories('de')
        cids = set([category.pk for category in categories])
        self.assertEqual(
            cids,
            set([self.category1.pk, self.category2.pk])
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
            ct.pk
        )

    def test_get_absolue_url(self):
        question_1_pk = self.question1.pk

        self.assertEqual(
            self.question1.get_absolute_url("en"),
            "/en/faq/1-example/{pk}/".format(pk=question_1_pk)
        )
        self.assertEqual(
            self.question1.get_absolute_url("de"),
            "/de/faq/1-beispiel/{pk}/".format(pk=question_1_pk)
        )

    def test_manager_filter_by_language(self):
        questions = Question.objects.filter_by_language('en')
        self.assertEqualItems(
            [q.pk for q in questions],
            [self.question1.pk]
        )

        questions = Question.objects.filter_by_language('de')
        self.assertEqualItems(
            [q.pk for q in questions],
            [self.question1.pk, self.question2.pk]
        )

    def test_manager_filter_by_current_language(self):
        with override("en"):
            questions = Question.objects.filter_by_current_language()
            self.assertEqualItems(
                [q.pk for q in questions],
                [self.question1.pk]
            )

        with override("de"):
            questions = Question.objects.filter_by_current_language()
            self.assertEqualItems(
                [q.pk for q in questions],
                [self.question1.pk, self.question2.pk]
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

    def test_fetch_faq_translations_fallbacks(self):
        """Test we can fetch arbitrary translations of the question and
        its category."""

        # Question and Category 1 do not exist in french
        # we expect to fallback to english
        with override("fr"):
            question_1_fr = self.reload(self.question1)
            category_1_fr = self.reload(self.question1.category)

            self.assertEqual(
                question_1_fr.safe_translation_getter('title', any_language=True),
                self.data["question1"]["en"]["title"]
            )
            self.assertEqual(
                question_1_fr.safe_translation_getter('answer_text', any_language=True),
                self.data["question1"]["en"]["answer_text"]
            )
            self.assertEqual(
                category_1_fr.safe_translation_getter('name', any_language=True),
                self.data["category1"]["en"]["name"]
            )
            self.assertEqual(
                category_1_fr.safe_translation_getter('slug', any_language=True),
                self.data["category1"]["en"]["slug"]
            )

        # Question and Category 2 do not exist in english
        # we expect to fallback to german
        with override("en"):
            question_2_en = self.reload(self.question2)
            category_2_en = self.reload(self.question2.category)

            self.assertEqual(
                question_2_en.safe_translation_getter('title', any_language=True),
                self.data["question2"]["de"]["title"]
            )
            self.assertEqual(
                question_2_en.safe_translation_getter('answer_text', any_language=True),
                self.data["question2"]["de"]["answer_text"]
            )
            self.assertEqual(
                category_2_en.safe_translation_getter('name', any_language=True),
                self.data["category2"]["de"]["name"]
            )
            self.assertEqual(
                category_2_en.safe_translation_getter('slug', any_language=True),
                self.data["category2"]["de"]["slug"]
            )
