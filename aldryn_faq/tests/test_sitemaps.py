# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase  # , TransactionTestCase
from django.utils.encoding import force_text

# from cms.utils.i18n import force_language

from hvad.test_utils.context_managers import LanguageOverride

from aldryn_faq.models import Category, Question, get_slug_in_language
from aldryn_faq.sitemaps import FAQCategoriesSitemap, FAQQuestionsSitemap

from .test_base import *  # flake8: noqa


class TestSitemap(AldrynFaqTestMixin, TestCase):

    def test_categories_sitemap_items(self):
        categories = FAQCategoriesSitemap().items()
        self.assertListContentsEqual(
            [category.id for category in categories],
            [self.category.id, self.category2.id]
        )

    def test_questions_sitemap_items(self):
        questions = FAQQuestionsSitemap().items()
        self.assertListContentsEqual(
            [question.id for question in questions],
            [self.question.id, self.question2.id]
        )
