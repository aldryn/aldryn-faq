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
        language = get_language_from_request(request, check_path=True)
        categories = Category.objects.active_translations(
            language_code=language).distinct()

        if hasattr(self, 'instance') and self.instance:
            #
            # If self has a property `instance`, then we're using django CMS
            # 3.0.12 or later, which supports using CMSAttachMenus on multiple,
            # apphook'ed pages, each with their own apphook configuration. So,
            # here we modify the queryset to reflect this.
            #
            app = apphook_pool.get_apphook(self.instance.application_urls)
            config = app.get_config(self.instance.application_namespace)
            if config:
                categories = categories.filter(appconfig=config)

        for category in categories:
            node = NavigationNode(
                category.safe_translation_getter(
                    'name', language_code=language),
                category.get_absolute_url(language=language),
                category.pk,
            )
            nodes.append(node)
            for question in category.questions.all():
                node = NavigationNode(
                    question.safe_translation_getter(
                        'title', language_code=language),
                    question.get_absolute_url(language=language),
                    # NOTE: We're adding 1 million here to avoid clashing with
                    # the category IDs.
                    category.pk * 1000000 + question.pk,
                    category.pk,
                )
                nodes.append(node)

        return nodes

menu_pool.register_menu(FaqCategoryMenu)
