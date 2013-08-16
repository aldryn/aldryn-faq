# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class FaqApp(CMSApp):
    name = _('FAQ')
    urls = ['aldryn_faq.urls']
    app_name = 'aldryn_faq'

apphook_pool.register(FaqApp)
