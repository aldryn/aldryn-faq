# -*- coding: utf-8 -*-
from django.utils.translation import get_language

from hvad.manager import TranslationManager


class RelatedManager(TranslationManager):

    def filter_by_language(self, language):
        return self.language(language)

    def filter_by_current_language(self):
        return self.filter_by_language(get_language())


class CategoryManager(TranslationManager):

    def get_categories(self, language=None):
        categories = self.language(language).prefetch_related('questions')

        for category in categories:
            category.count = (category.questions
            .filter_by_language(language).count())
        return sorted(categories, key=lambda x: -x.count)
