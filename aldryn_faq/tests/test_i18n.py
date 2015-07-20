# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import override

from .test_base import AldrynFaqTest


class TestGetAbsoluteUrls(AldrynFaqTest):

    def test_category_urls(self):

        with override('en'):
            category_1_url = self.category1.get_absolute_url()
            category_2_url = self.category2.get_absolute_url()

        self.assertEquals('/en/faq/1-example/', category_1_url)
        # category2 doesn't exist EN, so this should fallback to DE
        self.assertEquals('/en/faq/2-beispiel2/', category_2_url)

        with override('de'):
            category_1_url = self.category1.get_absolute_url()
            category_2_url = self.category2.get_absolute_url()

        self.assertEquals('/de/faq/1-beispiel/', category_1_url)
        self.assertEquals('/de/faq/2-beispiel2/', category_2_url)

        # Now, test that we can override the context with the language parameter
        with override('en'):
            category_1_url = self.category1.get_absolute_url(language="de")
            category_2_url = self.category2.get_absolute_url(language="de")

        self.assertEquals('/de/faq/1-beispiel/', category_1_url)
        self.assertEquals('/de/faq/2-beispiel2/', category_2_url)

        # For completeness, do the other way too
        with override('de'):
            category_1_url = self.category1.get_absolute_url(language="en")
            category_2_url = self.category2.get_absolute_url(language="en")

        self.assertEquals('/en/faq/1-example/', category_1_url)
        # category2 doesn't exist EN, so this should fallback to DE
        self.assertEquals('/en/faq/2-beispiel2/', category_2_url)

    def test_question_urls(self):

        with override('en'):
            question_1_url = self.question1.get_absolute_url()
            question_2_url = self.question2.get_absolute_url()

        question_1_pk = self.question1.pk
        question_2_pk = self.question2.pk

        self.assertEquals('/en/faq/1-example/{pk}/'.format(pk=question_1_pk), question_1_url)
        self.assertEquals('/en/faq/2-beispiel2/{pk}/'.format(pk=question_2_pk), question_2_url)

        with override('de'):
            question_1_url = self.question1.get_absolute_url()
            question_2_url = self.question2.get_absolute_url()

        self.assertEquals('/de/faq/1-beispiel/{pk}/'.format(pk=question_1_pk), question_1_url)
        self.assertEquals('/de/faq/2-beispiel2/{pk}/'.format(pk=question_2_pk), question_2_url)
