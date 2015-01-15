# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase  # , TransactionTestCase
from django.utils.encoding import force_text

# from cms.utils.i18n import force_language

from hvad.test_utils.context_managers import LanguageOverride

from aldryn_faq.models import Category, Question, get_slug_in_language

from .test_base import *  # flake8: noqa


class TestCategory(AldrynFaqTestMixin, TestCase):

    def test_unicode(self):
        with LanguageOverride('en'):
            category = self.reload(self.category)
            self.assertEqual(force_text(category), EN_CAT_NAME)
        with LanguageOverride('de'):
            category = self.reload(self.category)
            self.assertEqual(force_text(category), DE_CAT_NAME)

    def test_get_slug_in_language(self):
        self.assertIsNone(get_slug_in_language(None, 'en'), None)
        self.assertIsNone(get_slug_in_language(object, 'en'), None)
        self.assertEqual(
            get_slug_in_language(self.category, 'en'),
            EN_CAT_SLUG
        )
        self.assertEqual(
            get_slug_in_language(self.category, 'de'),
            DE_CAT_SLUG
        )
        # Test non-existent translation
        self.assertEqual(
            get_slug_in_language(self.category, 'qq'),
            None
        )

    def test_model_type_id(self):
        ct = ContentType.objects.get(app_label='aldryn_faq', model='category')
        self.assertEqual(
            self.category.model_type_id(),
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
            set([self.category.id])
        )

        # There's actually two categories in DE
        categories = Category.objects.get_categories('de')
        cids = set([category.id for category in categories])
        self.assertEqual(
            cids,
            set([self.category.id, self.category2.id])
        )


class TestQuestion(AldrynFaqTestMixin, TestCase):

    def test_unicode(self):
        with LanguageOverride('en'):
            question = self.reload(self.question)
            self.assertEqual(force_text(question), EN_QUE_TITLE)
        with LanguageOverride('de'):
            question = self.reload(self.question)
            self.assertEqual(force_text(question), DE_QUE_TITLE)

    def test_model_type_id(self):
        ct = ContentType.objects.get(app_label='aldryn_faq', model='question')
        self.assertEqual(
            self.question.model_type_id(),
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
        self.assertEqual(
            set(questions),
            set([self.question, self.question2])
        )
        pass

    def test_manager_filter_by_current_language(self):
        with LanguageOverride("en"):
            questions = Question.objects.filter_by_current_language()
            qids = set([question.id for question in questions])
            self.assertEqual(qids, set([self.question.id]))

        with LanguageOverride("de"):
            questions = Question.objects.filter_by_current_language()
            self.assertListContentsEqual(
                [question.id for question in questions],
                [self.question.id, self.question2.id]
            )


class TestFAQTranslations(AldrynFaqTestMixin, TestCase):

    def test_fetch_faq_translations(self):
        """Test we can fetch arbitrary translations of the question and
        its category."""
        # Can we target the EN values?
        with LanguageOverride("en"):
            question = self.reload(self.question)
            category = self.reload(self.question.category)
            self.assertEqual(question.title, EN_QUE_TITLE)
            self.assertEqual(question.answer_text, EN_QUE_ANSWER_TEXT)
            self.assertEqual(category.name, EN_CAT_NAME)
            self.assertEqual(category.slug, EN_CAT_SLUG)

        # And the DE values?
        with LanguageOverride("de"):
            question = self.reload(self.question)
            category = self.reload(self.question.category)
            self.assertEqual(question.title, DE_QUE_TITLE)
            self.assertEqual(question.answer_text, DE_QUE_ANSWER_TEXT)
            self.assertEqual(category.name, DE_CAT_NAME)
            self.assertEqual(category.slug, DE_CAT_SLUG)
