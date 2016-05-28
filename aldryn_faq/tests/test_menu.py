# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_faq.menu import FaqCategoryMenu
from menus.menu_pool import menu_pool

from .test_base import AldrynFaqTest


class TestMenu(AldrynFaqTest):

    def test_get_nodes(self):
        # Test that the EN version of the menu has only category1 and its
        # question1, and is shown in English.
        request = self.get_page_request(
            None, self.user, path='/en/', lang_code='en')
        try:
            renderer = menu_pool.get_renderer(request)
            menu = FaqCategoryMenu(renderer=renderer)
        except AttributeError:
            menu = FaqCategoryMenu()
        category1 = self.reload(self.category1, 'en')
        question1 = self.reload(self.question1, 'en')
        self.assertEqualItems(
            [menuitem.title for menuitem in menu.get_nodes(request)],
            [category1.name, question1.title]
        )

        # Test that the DE version has 2 categories and their questions that
        # they are shown in German.
        request = self.get_page_request(
            None, self.user, path='/de/', lang_code='de')
        try:
            renderer = menu_pool.get_renderer(request)
            menu = FaqCategoryMenu(renderer=renderer)
        except AttributeError:
            menu = FaqCategoryMenu()
        nodes = menu.get_nodes(request)
        self.assertEqualItems(
            [menuitem.title for menuitem in nodes],
            [self.category1.name, self.category2.name, self.question1.title,
                self.question2.title]
        )
