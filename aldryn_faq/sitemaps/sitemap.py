# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from ..models import Category, Question


class FAQCategoriesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Category.objects.all()


class FAQQuestionsSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Question.objects.all()
