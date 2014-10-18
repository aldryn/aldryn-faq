# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from aldryn_faq import request_faq_category_identifier, request_faq_question_identifier


@toolbar_pool.register
class FaqToolbar(CMSToolbar):

    def populate(self):

        def can(action, model):
            perm = 'aldryn_faq.%(action)s_%(model)s' % {'action': action, 'model': model}
            return self.request.user.has_perm(perm)

        if self.is_current_app and (can('add', 'category') or can('change', 'category')):
            menu = self.toolbar.get_or_create_menu('faq-app', _('FAQ'))

            if can('add', 'category'):
                menu.add_modal_item(_('Add category'), reverse('admin:aldryn_faq_category_add'))

            category = getattr(self.request, request_faq_category_identifier, None)

            if category and can('add', 'question'):
                params = ('?category=%s&language=%s' %
                          (category.pk, self.request.LANGUAGE_CODE))
                menu.add_modal_item(_('Add question'), reverse('admin:aldryn_faq_question_add') + params)
            if category and can('change', 'category'):
                url = reverse('admin:aldryn_faq_category_change', args=(category.pk,))
                menu.add_modal_item(_('Edit category'), url, active=True)

            question = getattr(self.request, request_faq_question_identifier, None)

            if question and can('change', 'question'):
                url = reverse('admin:aldryn_faq_question_change', args=(question.pk,))
                menu.add_modal_item(_('Edit question'), url, active=True)
