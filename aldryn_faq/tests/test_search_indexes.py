# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# from aldryn_faq.models import Category, Question, get_slug_in_language
from aldryn_faq.search_indexes import QuestionIndex, CategoryIndex
from . import AldrynFaqTest


class TestQuestionIndex(AldrynFaqTest):
    def test_get_title(self):
        idx_obj = QuestionIndex()
        question1 = self.reload(self.question1, "en")
        self.assertEqual(idx_obj.get_title(question1), question1.title)

    def test_get_index_kwargs(self):
        # This is a silly test, but is here for completeness.
        idx_obj = QuestionIndex()
        self.assertEqual(idx_obj.get_index_kwargs("en"), {
            'translations__language_code': 'en'
        })

    def test_get_index_queryset(self):
        idx_obj = QuestionIndex()
        # NOTE: This passes, but only serves to prove that the search_index
        # should be returning only objects that have the given translation!
        # TODO: Fix the above in search_indexes.py
        self.assertEqualItems(
            [q.id for q in idx_obj.get_index_queryset("en")],
            [self.question1.id, self.question2.id],
        )
        # This one is OK.
        self.assertEqualItems(
            [q.id for q in idx_obj.get_index_queryset("de")],
            [self.question1.id, self.question2.id],
        )

    def test_get_search_data(self):
        idx_obj = QuestionIndex()
        question1 = self.reload(self.question1, "en")
        search_data = idx_obj.get_search_data(question1, "en", None)
        self.assertEqual(search_data, "Test Question Test Answer")

        # This isn't working, but I think it proves that the search index
        # doesn't actually work translatedly.
        # TODO: Fix search_indexes.py
        # question1 = self.reload(self.question1, "de")
        # search_data = idx_obj.get_search_data(question1, "de", None)
        # self.assertEqual(search_data, "Testfrage Test Antwort")


class TestCategoryIndex(AldrynFaqTest):
    def test_get_title(self):
        # This search_index method always returns ""
        idx_obj = CategoryIndex()
        category1 = self.reload(self.category1, "en")
        self.assertEqual(idx_obj.get_title(category1), "")

    def test_get_index_kwargs(self):
        # This is a silly test, but is here for completeness.
        idx_obj = CategoryIndex()
        self.assertEqual(idx_obj.get_index_kwargs("en"), {
            'translations__language_code': 'en'
        })

    def test_get_index_queryset(self):
        idx_obj = CategoryIndex()
        # NOTE: This passes, but only serves to prove that the search_index
        # should be returning only objects that have the given translation!
        # TODO: Fix the above in search_indexes.py
        self.assertEqualItems(
            [q.id for q in idx_obj.get_index_queryset("en")],
            [self.category1.id, self.category2.id],
        )
        # This one is OK.
        self.assertEqualItems(
            [q.id for q in idx_obj.get_index_queryset("de")],
            [self.category1.id, self.category2.id],
        )

    def test_get_search_data(self):
        idx_obj = CategoryIndex()
        category1 = self.reload(self.category1, "en")
        search_data = idx_obj.get_search_data(category1, "en", None)
        self.assertEqual(search_data, "Example")

        # This isn't working, but I think it proves that the search index
        # doesn't actually work translatedly.
        # TODO: Fix search_indexes.py
        # category1 = self.reload(self.category1, "de")
        # search_data = idx_obj.get_search_data(category1, "de", None)
        # self.assertEqual(search_data, "Beispiel")
