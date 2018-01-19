# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import override

from cms.utils.i18n import force_language

from aldryn_faq.models import get_slug_in_language

from .test_base import AldrynFaqTest


class TestGetAbsoluteUrls(AldrynFaqTest):

    def test_category_urls(self):
        category_1 = self.category1
        category_2 = self.category2

        with override('en'):
            category_1_url_en = reverse(
                'aldryn_faq:faq-category',
                kwargs={
                    'category_pk': category_1.pk,
                    'category_slug': get_slug_in_language(category_1, 'en'),
                }
            )

            category_2_url_fallback_de = reverse(
                'aldryn_faq:faq-category',
                kwargs={
                    'category_pk': category_2.pk,
                    'category_slug': get_slug_in_language(category_2, 'de'),
                }
            )

            self.assertEquals(self.category1.get_absolute_url(), category_1_url_en)
            # category2 doesn't exist EN, so this should fallback to DE
            self.assertEquals(self.category2.get_absolute_url(), category_2_url_fallback_de)

        with override('de'):
            category_1_url_de = reverse(
                'aldryn_faq:faq-category',
                kwargs={
                    'category_pk': category_1.pk,
                    'category_slug': get_slug_in_language(category_1, 'de'),
                }
            )

            category_2_url_de = reverse(
                'aldryn_faq:faq-category',
                kwargs={
                    'category_pk': category_2.pk,
                    'category_slug': get_slug_in_language(category_2, 'de'),
                }
            )

            self.assertEquals(self.category1.get_absolute_url(), category_1_url_de)
            self.assertEquals(self.category2.get_absolute_url(), category_2_url_de)

        # test that we can override the context with the language parameter
        with override('en'):
            self.assertEquals(self.category1.get_absolute_url(language='de'), category_1_url_de)
            self.assertEquals(self.category2.get_absolute_url(language='de'), category_2_url_de)

        # For completeness, do the other way too
        with override('de'):
            self.assertEquals(self.category1.get_absolute_url(language='en'), category_1_url_en)
            # category2 doesn't exist EN, so this should fallback to DE
            self.assertEquals(self.category2.get_absolute_url(language='en'), category_2_url_fallback_de)

    def test_category_urls_fallbacks(self):
        category_1 = self.category1
        category_2 = self.category2

        with force_language('en'):
            category_2_url_fallback_de = reverse(
                'aldryn_faq:faq-category',
                kwargs={
                    'category_pk': category_2.pk,
                    'category_slug': get_slug_in_language(category_2, 'de'),
                }
            )

        with force_language('fr'):
            category_1_url_fallback_fr = reverse(
                'aldryn_faq:faq-category',
                kwargs={
                    'category_pk': category_1.pk,
                    'category_slug': get_slug_in_language(category_1, 'en'),
                }
            )

        # category 2 is not translated in english
        # so given our test fallback config
        # this should fallback to the german category
        self.assertEqual(category_2.get_absolute_url("en"), category_2_url_fallback_de)

        # category 1 is not translated in french
        # so given our test fallback config
        # this should fallback to the english category
        self.assertEqual(category_1.get_absolute_url("fr"), category_1_url_fallback_fr)

        with self.assertRaises(NoReverseMatch):
            # this should raise a NoRerverseMatch error
            # because category 2 is not translated in french
            # so it falls back to english which also does not exist
            category_2.get_absolute_url("fr")

    def test_question_urls(self):
        question_1 = self.question1
        category_1 = question_1.category

        question_2 = self.question2
        category_2 = question_2.category

        with override('en'):
            question_1_url_en = reverse(
                'aldryn_faq:faq-answer',
                kwargs={
                    'category_pk': category_1.pk,
                    'category_slug': get_slug_in_language(category_1, 'en'),
                    'pk': question_1.pk,
                }
            )

            question_2_url_en = reverse(
                'aldryn_faq:faq-answer',
                kwargs={
                    'category_pk': category_2.pk,
                    'category_slug': get_slug_in_language(category_2, 'de'),
                    'pk': question_2.pk,
                }
            )

            self.assertEquals(question_1.get_absolute_url(), question_1_url_en)
            self.assertEquals(question_2.get_absolute_url(), question_2_url_en)

        with override('de'):
            question_1_url_de = reverse(
                'aldryn_faq:faq-answer',
                kwargs={
                    'category_pk': category_1.pk,
                    'category_slug': get_slug_in_language(category_1, 'de'),
                    'pk': question_1.pk,
                }
            )

            question_2_url_de = reverse(
                'aldryn_faq:faq-answer',
                kwargs={
                    'category_pk': category_2.pk,
                    'category_slug': get_slug_in_language(category_2, 'de'),
                    'pk': question_2.pk,
                }
            )

            self.assertEquals(question_1.get_absolute_url(), question_1_url_de)
            self.assertEquals(question_2.get_absolute_url(), question_2_url_de)

    def test_question_urls_fallbacks(self):
        question_1 = self.question1
        category_1 = question_1.category

        question_2 = self.question2
        category_2 = question_2.category

        with force_language('en'):
            question_2_url_fallback_de = reverse(
                'aldryn_faq:faq-answer',
                kwargs={
                    'category_pk': category_2.pk,
                    'category_slug': get_slug_in_language(category_2, 'de'),
                    'pk': question_2.pk,
                }
            )

        with force_language('fr'):
            question_1_url_fallback_fr = reverse(
                'aldryn_faq:faq-answer',
                kwargs={
                    'category_pk': category_1.pk,
                    'category_slug': get_slug_in_language(category_1, 'en'),
                    'pk': question_1.pk,
                }
            )

        # question 2 is not translated in english
        # so given our test fallback config
        # this should fallback to the german category
        self.assertEqual(self.question2.get_absolute_url("en"), question_2_url_fallback_de)

        # question 1 is not translated in french
        # so given our test fallback config
        # this should fallback to the english category
        self.assertEqual(self.question1.get_absolute_url("fr"), question_1_url_fallback_fr)

        with self.assertRaises(NoReverseMatch):
            # this should raise a NoRerverseMatch error
            # because category 2 is not translated in french
            # so it falls back to english which also does not exist
            question_2.get_absolute_url("fr")
