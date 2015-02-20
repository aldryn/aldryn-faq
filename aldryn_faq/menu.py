# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import (
    get_language_from_request,
    ugettext_lazy as _,
)

from cms.menu_bases import CMSAttachMenu
from cms.apphook_pool import apphook_pool
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Category


class FaqCategoryMenu(CMSAttachMenu):
    name = _('FAQ')

    def get_nodes(self, request):
        nodes = []
        lang = get_language_from_request(request, check_path=True)
        categories = Category.objects.translated(lang)

        if hasattr(self, 'instance'):
            #
            # If self has a property `instance`, then we're using django CMS
            # 3.1.0 or later, which supports using CMSAttachMenus on multiple,
            # apphook'ed pages, each with their own apphook configuration. So,
            # here we modify the queryset to reflect this.
            #
            app = apphook_pool.get_apphook(self.instance.application_urls)
            config = app.get_config(self.instance.application_namespace)
            if config:
                categories = categories.filter(
                    appconfig__namespace=config.namespace
                )
        else:
            print('FaqCategoryMenu does not have the property: instance!')

        for category in categories:
            node = NavigationNode(
                category.safe_translation_getter('name', language_code=lang),
                category.get_absolute_url(language=lang),
                category.safe_translation_getter('slug', language_code=lang),
            )
            nodes.append(node)
        return nodes

menu_pool.register_menu(FaqCategoryMenu)
