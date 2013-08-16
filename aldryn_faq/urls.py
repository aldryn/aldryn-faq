# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.FAQView.as_view(), name='faq'),
)
