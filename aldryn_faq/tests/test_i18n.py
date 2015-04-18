# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import override

from .test_base import AldrynFaqTest


class TestGetAbsoluteUrls(AldrynFaqTest):

    def test_category_urls(self):

        with override('en'):
            url1 = self.category1.get_absolute_url()
            url2 = self.category2.get_absolute_url()
        self.assertEquals('/en/faq/example/', url1)
        # category2 doesn't exist EN, so this should fallback to DE
        self.assertEquals('/de/faq/beispiel2/', url2)

        with override('de'):
            url1 = self.category1.get_absolute_url()
            url2 = self.category2.get_absolute_url()
        self.assertEquals('/de/faq/beispiel/', url1)
        self.assertEquals('/de/faq/beispiel2/', url2)

        # Now, test that we can override the context with the language parameter
        with override('en'):
            url1 = self.category1.get_absolute_url(language="de")
            url2 = self.category2.get_absolute_url(language="de")
        self.assertEquals('/de/faq/beispiel/', url1)
        self.assertEquals('/de/faq/beispiel2/', url2)

        # For completeness, do the other way too
        with override('de'):
            url1 = self.category1.get_absolute_url(language="en")
            url2 = self.category2.get_absolute_url(language="en")
        self.assertEquals('/en/faq/example/', url1)
        # category2 doesn't exist EN, so this should fallback to DE
        self.assertEquals('/de/faq/beispiel2/', url2)

    def test_question_urls(self):

        with override('en'):
            url1 = self.question1.get_absolute_url()
            url2 = self.question2.get_absolute_url()

        pk1 = self.question1.pk
        pk2 = self.question2.pk

        self.assertEquals('/en/faq/example/{pk}/'.format(pk=pk1), url1)
        # neigher category2 nor question2 exist in EN, so, this should return
        # the DE fallback to the question.
        self.assertEquals('/de/faq/beispiel2/{pk}/'.format(pk=pk2), url2)

        with override('de'):
            url1 = self.question1.get_absolute_url()
            url2 = self.question2.get_absolute_url()

        self.assertEquals('/de/faq/beispiel/{pk}/'.format(pk=pk1), url1)
        self.assertEquals('/de/faq/beispiel2/{pk}/'.format(pk=pk2), url2)
