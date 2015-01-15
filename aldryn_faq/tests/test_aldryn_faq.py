# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase  # , TransactionTestCase
from django.utils.encoding import force_text

# from cms.utils.i18n import force_language

from hvad.test_utils.context_managers import LanguageOverride

from aldryn_faq.models import Category, Question, get_slug_in_language

EN_CAT_NAME = "Example"
EN_CAT_SLUG = "example"
EN_QUE_TITLE = "Test Question"
EN_QUE_ANSWER_TEXT = "Test Answer"

DE_CAT_NAME = "Beispiel"
DE_CAT_SLUG = "beispiel"

# This should NOT have a EN translation
DE_CAT_NAME2 = "Beispiel2"
DE_CAT_SLUG2 = "beispiel2"

DE_QUE_TITLE = "Testfrage"
DE_QUE_ANSWER_TEXT = "Test Antwort"

# This should NOT have a EN translation
DE_QUE_TITLE2 = "Testfrage2"
DE_QUE_ANSWER_TEXT2 = "Test Antwort2"


class AldrynFaqTestMixin(object):

    @staticmethod
    def reload(object):
        """Simple convenience method for re-fetching an object from the ORM."""
        return object.__class__.objects.get(id=object.id)

    def mktranslation(self, obj, lang, **kwargs):
        """Simple method of adding a translation to an existing object."""
        obj.translate(lang)
        for k, v in kwargs.iteritems():
            setattr(obj, k, v)
        obj.save()

    def setUp(self):
        """Setup a prebuilt and translated Question with Category
        for testing."""
        with LanguageOverride("en"):
            self.category = Category(**{
                "name": EN_CAT_NAME,
                "slug": EN_CAT_SLUG
            })
            self.category.save()
            self.question = Question(**{
                "title": EN_QUE_TITLE,
                "answer_text": EN_QUE_ANSWER_TEXT,
            })
            self.question.category = self.category
            self.question.save()

        # Make a DE translation of the category
        self.mktranslation(self.category, "de", **{
            "name": DE_CAT_NAME,
            "slug": DE_CAT_SLUG,
        })
        # Make a DE translation of the question
        self.mktranslation(self.question, "de", **{
            "title": DE_QUE_TITLE,
            "answer_text": DE_QUE_ANSWER_TEXT,
        })

        with LanguageOverride("de"):
            # Make a DE-only Category
            self.category2 = Category(**{
                "name": DE_CAT_NAME2,
                "slug": DE_CAT_SLUG2
            })
            self.category2.save()

            # Make a DE-only Question
            self.question2 = Question(**{
                "title": DE_QUE_TITLE2,
                "answer_text": DE_QUE_ANSWER_TEXT2,
            })
            self.question2.category = self.category2
            self.question2.save()


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
            qids = set([question.id for question in questions])
            self.assertEqual(qids, set([self.question.id, self.question2.id]))


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
