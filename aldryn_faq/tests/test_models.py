# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase  # , TransactionTestCase
from django.utils.encoding import force_text

# from cms.utils.i18n import force_language

from hvad.test_utils.context_managers import LanguageOverride

from aldryn_faq.models import Category, Question, get_slug_in_language

from . import AldrynFaqTestMixin, TestUtilityMixin


class TestCategory(AldrynFaqTestMixin, TestCase):

    def test_unicode(self):
        with LanguageOverride('en'):
            category1 = self.reload(self.category1)
            self.assertEqual(force_text(category1), self.data["category1"]["en"]["name"])
        with LanguageOverride('de'):
            category1 = self.reload(self.category1)
            self.assertEqual(force_text(category1), self.data["category1"]["de"]["name"])

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
        # TODO: Make these tests run.
        pass
        # self.assertEqual(
        #     self.category.get_absolute_url(),
        #     ""
        # )

    def test_manager_get_categories(self):
        # Test case when no language is passed.
        # TODO: This doesn't actually pass
        # self.assertEqual(
        #     set(Category.objects.get_categories()),
        #     set([self.category, self.category2])
        # )

        # Test case of requesting objects of only a single language
        categories = Category.objects.get_categories('en')
        cids = set([category.id for category in categories])
        self.assertEqual(
            cids,
            set([self.category1.id])
        )

        # There's actually two categories in DE
        categories = Category.objects.get_categories('de')
        cids = set([category.id for category in categories])
        self.assertEqual(
            cids,
            set([self.category1.id, self.category2.id])
        )


class TestQuestion(AldrynFaqTestMixin, TestUtilityMixin, TestCase):

    def test_unicode(self):
        with LanguageOverride('en'):
            question1 = self.reload(self.question1)
            self.assertEqual(
                force_text(question1),
                self.data["question1"]["en"]["title"]
            )
        with LanguageOverride('de'):
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
        # TODO: Make these tests run.
        pass
        # self.assertEqual(
        #     self.category.get_absolute_url(),
        #     ""
        # )

    def test_manager_filter_by_language(self):
        # TODO: This fails, why?
        # questions = Question.objects.filter_by_language('en')
        # self.assertEqual(questions, [self.question])

        questions = Question.objects.filter_by_language('de')
        self.assertListContentsEqual(
            list(questions),
            [self.question1, self.question2]
        )
        pass

    def test_manager_filter_by_current_language(self):
        with LanguageOverride("en"):
            questions = Question.objects.filter_by_current_language()
            self.assertListContentsEqual(
                [question.id for question in questions],
                [self.question1.id]
            )

        with LanguageOverride("de"):
            questions = Question.objects.filter_by_current_language()
            self.assertListContentsEqual(
                [question.id for question in questions],
                [self.question1.id, self.question2.id]
            )


class TestFAQTranslations(AldrynFaqTestMixin, TestCase):

    def test_fetch_faq_translations(self):
        """Test we can fetch arbitrary translations of the question and
        its category."""
        # Can we target the EN values?
        with LanguageOverride("en"):
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
        with LanguageOverride("de"):
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
