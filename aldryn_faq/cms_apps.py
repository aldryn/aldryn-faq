# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool

from .models import FaqConfig


class FaqApp(CMSConfigApp):
    name = _('FAQ')
    app_name = 'aldryn_faq'
    app_config = FaqConfig
    urls = ['aldryn_faq.urls']  # COMPAT: CMS3.2

    def get_urls(self, *args, **kwargs):
        return self.urls


apphook_pool.register(FaqApp)
