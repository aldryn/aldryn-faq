# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_faq.sitemaps import FAQCategoriesSitemap, FAQQuestionsSitemap

from .test_base import AldrynFaqTest


class TestSitemap(AldrynFaqTest):

    def test_categories_sitemap_items(self):
        categories = [cat.id for cat in FAQCategoriesSitemap().items()]
        self.assertEqualItems(
            categories,
            [self.category1.id, self.category2.id]
        )

    def test_questions_sitemap_items(self):
        questions = [que.id for que in FAQQuestionsSitemap().items()]
        self.assertEqualItems(
            questions,
            [self.question1.id, self.question2.id]
        )
