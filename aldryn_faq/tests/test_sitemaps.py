# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase

from aldryn_faq.sitemaps import FAQCategoriesSitemap, FAQQuestionsSitemap

from . import AldrynFaqTestMixin, TestUtilityMixin


class TestSitemap(AldrynFaqTestMixin, TestUtilityMixin, TestCase):

    def test_categories_sitemap_items(self):
        categories = FAQCategoriesSitemap().items()
        self.assertListContentsEqual(
            [category.id for category in categories],
            [self.category1.id, self.category2.id]
        )

    def test_questions_sitemap_items(self):
        questions = FAQQuestionsSitemap().items()
        self.assertListContentsEqual(
            [question.id for question in questions],
            [self.question1.id, self.question2.id]
        )
