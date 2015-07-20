# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.test.client import RequestFactory
from django.utils.translation import override

from ..views import FaqByCategoryView, FaqAnswerView

from .test_base import AldrynFaqTest


class TestFaqByCategoryView(AldrynFaqTest):

    def test_view_context(self):
        """Tests that the FaqByCategoryView produces the correct context."""
        category_1 = self.reload(self.category1, "en")
        category_1_url = category_1.get_absolute_url()

        question_1 = self.reload(self.question1, "en")

        request = self.get_page_request(
            page=self.page,
            user=self.user,
            path=category_1_url,
        )

        url_kwargs = resolve(category_1_url).kwargs

        try:
            response = FaqByCategoryView.as_view()(request, **url_kwargs)
        except Http404:
            self.fail('Could not find category')

        self.assertEqualItems(
            response.context_data['object_list'],
            [question_1, ],
        )

    def test_view_old_format_redirect(self):
        """
        Tests that the FaqByCategoryView redirects user
        when accessed with old category url format
        """
        category_1 = self.reload(self.category1, "en")

        kwargs = {"category_slug": category_1.slug}

        with override('en'):
            category_1_url_name = '{0}:faq-category'.format(self.app_config.namespace)
            category_1_url = reverse(category_1_url_name, kwargs=kwargs)

        request = self.get_page_request(
            page=self.page,
            user=self.user,
            path=category_1_url,
        )

        response = FaqByCategoryView.as_view()(request, **kwargs)

        self.assertEquals(response.status_code, 301)


class TestFaqAnswerView(AldrynFaqTest):

    def test_view_context(self):
        """Tests that the FaqByCategoryView produces the correct context."""
        question_1 = self.reload(self.question1, "en")
        question_1_url = question_1.get_absolute_url("en")

        url_kwargs = resolve(question_1_url).kwargs

        request = self.get_page_request(
            page=self.page,
            user=self.user,
            path=question_1_url,
        )

        response = FaqAnswerView.as_view()(request, **url_kwargs)

        self.assertEqual(
            response.context_data['object'],
            question_1,
        )

    def test_view_old_format_redirect(self):
        """
        Tests that the TestFaqAnswerView redirects user
        when accessed with old category url format
        """
        category_1 = self.reload(self.category1, "en")
        question_1 = self.reload(self.question1, "en")

        kwargs = {
            "category_slug": category_1.slug,
            "pk": question_1.pk
        }

        with override('en'):
            url_name = '{0}:faq-answer'.format(self.app_config.namespace)
            question_1_url = reverse(url_name, kwargs=kwargs)

        request = self.get_page_request(
            page=self.page,
            user=self.user,
            path=question_1_url,
        )

        response = FaqAnswerView.as_view()(request, **kwargs)

        self.assertEquals(response.status_code, 301)

    def test_answer_match_category(self):
        """
        Tests that the question id given in url
        belongs to the given category, if not then 404 is raised.
        """
        category_1 = self.reload(self.category1, "de")
        question_2 = self.reload(self.question2, "de")

        kwargs = {
            "category_pk": category_1.pk,
            "category_slug": category_1.slug,
            "pk": question_2.pk
        }

        with override('de'):
            url_name = '{0}:faq-answer'.format(self.app_config.namespace)
            question_2_invalid_url = reverse(url_name, kwargs=kwargs)

        request = self.get_page_request(
            page=self.page,
            user=self.user,
            path=question_2_invalid_url,
        )

        with self.assertRaises(Http404):
            FaqAnswerView.as_view()(request, **kwargs)
