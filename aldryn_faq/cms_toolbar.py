# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from aldryn_apphooks_config.utils import get_app_instance
from cms.utils.urlutils import admin_reverse

from aldryn_faq import (
    request_faq_category_identifier,
    request_faq_question_identifier,
)
from .models import Category, FaqConfig


@toolbar_pool.register
class FaqToolbar(CMSToolbar):
    watch_models = (Category, )

    def __get_newsblog_config(self):
        try:
            __, config = get_app_instance(self.request)
            if not isinstance(config, FaqConfig):
                # This is not the app_hook you are looking for.
                return None
        except ImproperlyConfigured:
            # There is no app_hook at all.
            return None

        return config

    def populate(self):
        def can(action, model):
            perm = 'aldryn_faq.%(action)s_%(model)s' % {
                'action': action, 'model': model}
            return self.request.user.has_perm(perm)

        config = self.__get_newsblog_config()
        if not config:
            return

        menu = self.toolbar.get_or_create_menu('faq-app', _('FAQ'))

        if can('change', 'faqconfig'):
            menu.add_modal_item(
                _('Configure application'),
                url=admin_reverse(
                    'aldryn_faq_faqconfig_change',
                    args=(config.pk, )
                ),
            )

        if can('add', 'category') or can('change', 'category'):
            if can('add', 'category'):
                menu.add_modal_item(
                    _('Add category'),
                    url=admin_reverse('aldryn_faq_category_add')
                )

        category = getattr(self.request, request_faq_category_identifier, None)

        if category and can('change', 'category'):
            url = reverse(
                'admin:aldryn_faq_category_change',
                args=(category.pk,),
            )
            menu.add_modal_item(_('Edit category'), url, active=True)

        if category and can('add', 'question'):
            params = ('?category=%s&language=%s' %
                      (category.pk, self.request.LANGUAGE_CODE))
            menu.add_modal_item(
                _('Add question'),
                admin_reverse('aldryn_faq_question_add') + params
            )

        question = getattr(self.request, request_faq_question_identifier, None)

        if question and can('change', 'question'):
            url = reverse(
                'admin:aldryn_faq_question_change', args=(question.pk,))
            menu.add_modal_item(_('Edit question'), url, active=True)
