# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import FaqAnswerView, FaqByCategoryView, FaqByCategoryListView


urlpatterns = patterns('',
    url(r'^$', FaqByCategoryListView.as_view(), name='faq-category-list'),
    url(
        r'^(?P<category_slug>[-\w]+)/$',
        FaqByCategoryView.as_view(),
        name='faq-category'
    ),
    url(
        r'^(?P<category_pk>[0-9]+)/(?P<category_slug>[-\w]+)/$',
        FaqByCategoryView.as_view(),
        name='faq-category'
    ),
    url(
        r'^(?P<category_slug>[-\w]+)/(?P<pk>[0-9]+)/$',
        FaqAnswerView.as_view(),
        name='faq-answer'
    ),
)
