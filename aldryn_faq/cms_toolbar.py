# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from aldryn_blog import request_post_identifier
from aldryn_faq import request_faq_category_identifier


@toolbar_pool.register
class FaqToolbar(CMSToolbar):
    def populate(self):
        def can(action, model):
            perm = 'aldryn_faq.%(action)s_%(model)s' % {'action': action,
                                                        'model': model}
            return self.request.user.has_perm(perm)

        if self.is_current_app and (can('add', 'category')
                                    or can('change', 'category')):
            menu = self.toolbar.get_or_create_menu('faq-app', _('FAQ'))
            if can('add', 'category'):
                menu.add_modal_item(_('Add category'), reverse('admin:aldryn_faq_category_add') + '?_popup')

            category = getattr(self.request, request_faq_category_identifier, None)
            if category and can('change', 'category'):
                url = reverse('admin:aldryn_faq_category_change', args=(category.pk,)) + '?_popup'
                menu.add_modal_item(_('Edit category'), url, active=True)