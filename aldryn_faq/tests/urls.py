# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from djangocms_helper.urls import urlpatterns


urlpatterns += [
    url(r'^faq/', include('aldryn_faq.urls', namespace='aldryn_faq')),
]
