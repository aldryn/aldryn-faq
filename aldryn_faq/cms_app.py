# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool

from .menu import FaqCategoryMenu
from .models import FaqConfig


class FaqApp(CMSConfigApp):
    name = _('FAQ')
    urls = ['aldryn_faq.urls']
    menus = [FaqCategoryMenu]
    app_name = 'aldryn_faq'
    app_config = FaqConfig

apphook_pool.register(FaqApp)
