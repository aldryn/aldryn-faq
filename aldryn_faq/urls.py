# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from . import views
from aldryn_faq.views import FaqByCategoryView

urlpatterns = patterns(
    '',
    url(r'^$', views.FAQView.as_view(), name='faq'),
    url(r'^(?P<category_slug>[-\w]+)/$', FaqByCategoryView.as_view(), name='faq-category'),
)
