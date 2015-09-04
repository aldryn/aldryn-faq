# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import FaqAnswerView, FaqByCategoryView, FaqByCategoryListView


urlpatterns = patterns('',
    url(r'^$', FaqByCategoryListView.as_view(), name='faq-category-list'),


    # 1/
    url(
        r'^(?P<category_pk>\d+)/$',
        FaqByCategoryView.as_view(),
        name='faq-category'
    ),
    # 1/2/
    url(
        r'^(?P<category_pk>\d+)/(?P<pk>\d+)/$',
        FaqAnswerView.as_view(),
        name='faq-answer'
    ),
    # 1/question-slug/
    url(
        r'^(?P<category_pk>\d+)/(?P<slug>[-\w]+)/$',
        FaqAnswerView.as_view(),
        name='faq-answer'
    ),

    # NOTE: This set must appear before the 'category-slug/*' set below

    # 1-category-slug/
    url(
        r'^(?P<category_pk>\d+)-(?P<category_slug>[-\w]+)/$',
        FaqByCategoryView.as_view(),
        name='faq-category'
    ),
    # 1-category-slug/2/
    url(
        r'^(?P<category_pk>\d+)-(?P<category_slug>[-\w]+)/(?P<pk>\d+)/$',
        FaqAnswerView.as_view(),
        name='faq-answer'
    ),
    # 1-category-slug/question-slug/
    url(
        r'^(?P<category_pk>\d+)-(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        FaqAnswerView.as_view(),
        name='faq-answer'
    ),


    # category-slug/
    url(
        r'^(?P<category_slug>[-\w]+)/$',
        FaqByCategoryView.as_view(),
        name='faq-category'
    ),
    # category-slug/2/
    url(
        r'^(?P<category_slug>[-\w]+)/(?P<pk>\d+)/$',
        FaqAnswerView.as_view(),
        name='faq-answer'
    ),
    # category-slug/question-slug/
    url(
        r'^(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        FaqAnswerView.as_view(),
        name='faq-answer'
    ),
)
