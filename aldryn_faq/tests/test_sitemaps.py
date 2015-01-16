# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_faq.sitemaps import FAQCategoriesSitemap, FAQQuestionsSitemap

from . import AldrynFaqTest


class TestSitemap(AldrynFaqTest):

    def test_categories_sitemap_items(self):
        categories = FAQCategoriesSitemap().items()
        self.assertItemsEqual(categories, [self.category1, self.category2])

    def test_questions_sitemap_items(self):
        questions = FAQQuestionsSitemap().items()
        self.assertItemsEqual(questions, [self.question1, self.question2])
