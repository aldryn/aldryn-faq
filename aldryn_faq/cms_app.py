# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool

from .models import FaqConfig


class FaqApp(CMSConfigApp):
    name = _('FAQ')
    urls = ['aldryn_faq.urls']
    app_name = 'aldryn_faq'
    app_config = FaqConfig

apphook_pool.register(FaqApp)
