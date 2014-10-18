# -*- coding: utf-8 -*-
from django.utils.translation import get_language_from_request, ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from cms.menu_bases import CMSAttachMenu

from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import Category


def clear_menu_cache(**kwargs):
    menu_pool.clear(all=True)


class FaqCategoryMenu(CMSAttachMenu):

    name = _('FAQ')

    def get_nodes(self, request):
        nodes = []
        language = get_language_from_request(request)
        categories = Category.objects.language(language)

        for category in categories:
            node = NavigationNode(category.name,
                                  category.get_absolute_url(),
                                  category.slug)
            nodes.append(node)
        return nodes


menu_pool.register_menu(FaqCategoryMenu)

post_save.connect(clear_menu_cache, sender=Category)
post_delete.connect(clear_menu_cache, sender=Category)
