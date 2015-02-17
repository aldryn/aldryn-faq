# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.utils.translation import override

from aldryn_faq.views import FaqByCategoryView, FaqAnswerView

from .test_base import AldrynFaqTest, CMSRequestBasedTest


class TestFaqByCategoryView(AldrynFaqTest, CMSRequestBasedTest):
    def test_as_view(self):
        """Tests that the FaqByCategoryView produces the correct context."""
        category1 = self.reload(self.category1, "en")
        question1 = self.reload(self.question1, "en")
        kwargs = {"category_slug": category1.slug}
        with override('en'):
            category1_url = reverse('aldryn_faq:faq-category', kwargs=kwargs)
        factory = RequestFactory()
        request = factory.get(category1_url)
        response = FaqByCategoryView.as_view()(request, **kwargs)
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
            url = reverse('aldryn_faq:faq-answer', kwargs=kwargs)
        factory = RequestFactory()
        request = factory.get(url)
        response = FaqAnswerView.as_view()(request, **kwargs)
        self.assertEqual(
            response.context_data['object'],
            question1,
        )
