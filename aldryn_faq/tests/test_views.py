# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.test.client import RequestFactory
from django.utils.translation import override

from ..views import FaqByCategoryView, FaqAnswerView

from .test_base import AldrynFaqTest, CMSRequestBasedTest


class TestFaqByCategoryView(AldrynFaqTest, CMSRequestBasedTest):
    def test_as_view(self):
        """Tests that the FaqByCategoryView produces the correct context."""
        category1 = self.reload(self.category1, "en")
        question1 = self.reload(self.question1, "en")

        kwargs = {"category_slug": category1.slug}
        with override('en'):
            category1_url = reverse(
                '{0}:faq-category'.format(self.app_config.namespace),
                kwargs=kwargs
            )
        factory = RequestFactory()
        request = factory.get(category1_url)
        request.user = self.user
        # We're not going through the middleware, and apphooks_config needs
        # 'current_page' to be set on the request objects, so...
        request.current_page = self.page
        try:
            response = FaqByCategoryView.as_view()(request, **kwargs)
        except Http404:
            self.fail('Could not find category')
        self.assertEqualItems(
            response.context_data['object_list'],
            [question1, ],
        )


class TestFaqAnswerView(AldrynFaqTest, CMSRequestBasedTest):
    def test_as_view(self):
        """Tests that the FaqAnswerView produces the correct context."""
        category1 = self.reload(self.category1, "en")
        question1 = self.reload(self.question1, "en")

        kwargs = {"category_slug": category1.slug, "pk": question1.id}
        with override('en'):
            url = reverse(
                '{0}:faq-answer'.format(self.app_config.namespace),
                kwargs=kwargs
            )
        factory = RequestFactory()
        request = factory.get(url)
        request.user = self.user
        # We're not going through the middleware, and apphooks_config needs
        # 'current_page' to be set on the request objects, so...
        request.current_page = self.page
        response = FaqAnswerView.as_view()(request, **kwargs)
        self.assertEqual(
            response.context_data['object'],
            question1,
        )
