# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import (
    get_language_from_request,
    ugettext_lazy as _,
)

from cms.menu_bases import CMSAttachMenu

from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Category


class FaqCategoryMenu(CMSAttachMenu):

    name = _('FAQ')

    def get_nodes(self, request):
        nodes = []
        lang = get_language_from_request(request, check_path=True)
        categories = Category.objects.translated(lang)

        for category in categories:
            node = NavigationNode(
                category.safe_translation_getter('name', language_code=lang),
                category.get_absolute_url(language=lang),
                category.safe_translation_getter('slug', language_code=lang),
            )
            nodes.append(node)
        return nodes

menu_pool.register_menu(FaqCategoryMenu)
