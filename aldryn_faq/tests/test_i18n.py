# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import override

from .test_base import AldrynFaqTest


class TestGetAbsoluteUrls(AldrynFaqTest):

    def test_category_urls(self):
        category_1_pk = self.category1.pk
        category_2_pk = self.category2.pk

        with override('en'):
            category_1_url = self.category1.get_absolute_url()
            category_2_url = self.category2.get_absolute_url()

        self.assertEquals('/en/faq/{cat}-example/'.format(
            cat=category_1_pk), category_1_url)
        # category2 doesn't exist EN, so this should fallback to DE
        self.assertEquals('/en/faq/{cat}-beispiel2/'.format(
            cat=category_2_pk), category_2_url)

        with override('de'):
            category_1_url = self.category1.get_absolute_url()
            category_2_url = self.category2.get_absolute_url()

        self.assertEquals('/de/faq/{cat}-beispiel/'.format(
            cat=category_1_pk), category_1_url)
        self.assertEquals('/de/faq/{cat}-beispiel2/'.format(
            cat=category_2_pk), category_2_url)

        # test that we can override the context with the language parameter
        with override('en'):
            category_1_url = self.category1.get_absolute_url(language="de")
            category_2_url = self.category2.get_absolute_url(language="de")

        self.assertEquals('/de/faq/{cat}-beispiel/'.format(
            cat=category_1_pk), category_1_url)
        self.assertEquals('/de/faq/{cat}-beispiel2/'.format(
            cat=category_2_pk), category_2_url)

        # For completeness, do the other way too
        with override('de'):
            category_1_url = self.category1.get_absolute_url(language="en")
            category_2_url = self.category2.get_absolute_url(language="en")

        self.assertEquals('/en/faq/{cat}-example/'.format(
            cat=category_1_pk), category_1_url)
        # category2 doesn't exist EN, so this should fallback to DE
        self.assertEquals('/en/faq/{cat}-beispiel2/'.format(
            cat=category_2_pk), category_2_url)

    def test_category_urls_fallbacks(self):
        category_1 = self.category1
        category_2 = self.category2

        # category 2 is not translated in english
        # so given our test fallback config
        # this should fallback to the german category
        self.assertEqual(
            category_2.get_absolute_url("en"),
            "/en/faq/{cat}-beispiel2/".format(cat=category_2.pk)
        )

        # category 1 is not translated in french
        # so given our test fallback config
        # this should fallback to the english category
        self.assertEqual(
            category_1.get_absolute_url("fr"),
            "/fr/faq/{cat}-example/".format(cat=category_1.pk)
        )

        with self.assertRaises(NoReverseMatch):
            # this should raise a NoRerverseMatch error
            # because category 2 is not translated in french
            # so it falls back to english which also does not exist
            category_2.get_absolute_url("fr")

    def test_question_urls(self):
        question_1_pk = self.question1.pk
        question_1_category_pk = self.question1.category_id

        question_2_pk = self.question2.pk
        question_2_category_pk = self.question2.category_id

        with override('en'):
            question_1 = self.reload(self.question1)
            question_1_url = question_1.get_absolute_url()

            question_2 = self.reload(self.question2)

            question_2_url = question_2.get_absolute_url()

        self.assertEquals('/en/faq/{cat_pk}-example/{pk}/'.format(
            cat_pk=question_1_category_pk, pk=question_1_pk), question_1_url)

        self.assertEquals('/en/faq/{cat_pk}-beispiel2/{pk}/'.format(
            cat_pk=question_2_category_pk, pk=question_2_pk), question_2_url)

        with override('de'):
            question_1 = self.reload(self.question1)
            question_1_url = question_1.get_absolute_url()

            question_2 = self.reload(self.question2)
            question_2_url = question_2.get_absolute_url()

        self.assertEquals('/de/faq/{cat_pk}-beispiel/{pk}/'.format(
            cat_pk=question_1_category_pk, pk=question_1_pk), question_1_url)

        self.assertEquals('/de/faq/{cat_pk}-beispiel2/{pk}/'.format(
            cat_pk=question_2_category_pk, pk=question_2_pk), question_2_url)

    def test_question_urls_fallbacks(self):
        question_1 = self.question1
        question_1_pk = question_1.pk
        question_1_category_pk = question_1.category_id

        question_2 = self.question2
        question_2_pk = question_2.pk
        question_2_category_pk = question_2.category_id

        # question 2 is not translated in english
        # so given our test fallback config
        # this should fallback to the german category
        self.assertEqual(
            question_2.get_absolute_url("en"),
            "/en/faq/{cat_pk}-beispiel2/{pk}/".format(
                cat_pk=question_2_category_pk, pk=question_2_pk)
        )

        # question 1 is not translated in french
        # so given our test fallback config
        # this should fallback to the english category
        self.assertEqual(
            question_1.get_absolute_url("fr"),
            "/fr/faq/{cat_pk}-example/{pk}/".format(
                cat_pk=question_1_category_pk, pk=question_1_pk)
        )

        with self.assertRaises(NoReverseMatch):
            # this should raise a NoRerverseMatch error
            # because category 2 is not translated in french
            # so it falls back to english which also does not exist
            question_2.get_absolute_url("fr")
