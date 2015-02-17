# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_faq.menu import FaqCategoryMenu
from django.utils.translation import (
    get_language_from_request,
)
from .test_base import AldrynFaqTest, CMSRequestBasedTest


class TestMenu(AldrynFaqTest, CMSRequestBasedTest):

    def test_get_nodes(self):
        # Test that the EN version of the menu has only category1 and is shown
        # in English.
        request = self.get_page_request(None, self.user, '/en/')
        menu = FaqCategoryMenu()
        category1 = self.reload(self.category1, 'en')
        self.assertEqualItems(
            [menuitem.title for menuitem in menu.get_nodes(request)],
            [category1.name]
        )

        # Test that the DE version has 2 categories and that they are shown in
        # German.
        request = self.get_page_request(None, self.user, '/de/')
        menu = FaqCategoryMenu()
        category1 = self.reload(self.category1, 'de')
        category2 = self.reload(self.category2, 'de')
        nodes = menu.get_nodes(request)
        self.assertEqualItems(
            [menuitem.title for menuitem in nodes],
            [category1.name, category2.name]
        )
