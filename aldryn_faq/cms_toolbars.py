# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, get_language_from_request

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.utils.i18n import force_language
from cms.utils.urlutils import admin_reverse

from aldryn_apphooks_config.utils import get_app_instance
from parler.models import TranslatableModel

from .models import Category, FaqConfig, Question


def get_obj_from_request(model, request,
                         pk_url_kwarg='pk',
                         slug_url_kwarg='slug',
                         slug_field='slug'):
    """
    Given a model and the request, try to extract and return an object
    from an available 'pk' or 'slug', or return None.

    Note that no checking is done that the view's kwargs really are for objects
    matching the provided model (how would it?) so use only where appropriate.
    """
    language = get_language_from_request(request, check_path=True)
    kwargs = request.resolver_match.kwargs
    mgr = model.objects
    if pk_url_kwarg in kwargs:
        return mgr.filter(pk=kwargs[pk_url_kwarg]).first()
    elif slug_url_kwarg in kwargs:
        # If the model is translatable, and the given slug is a translated
        # field, then find it the Parler way.
        filter_kwargs = {slug_field: kwargs[slug_url_kwarg]}
        translated_fields = model._parler_meta.get_translated_fields()
        if (issubclass(model, TranslatableModel) and
                slug_field in translated_fields):
            return mgr.active_translations(language, **filter_kwargs).first()
        else:
            # OK, do it the normal way.
            return mgr.filter(**filter_kwargs).first()
    else:
        return None


def get_admin_url(action, action_args=[], **url_args):
    """
    Convenience method for constructing admin-urls with GET parameters.

    :param action:      The admin url key for use in reverse. E.g.,
                        'aldryn_newsblog_edit_article'
    :param action_args: The url args for the reverse. E.g., [article.pk, ]
    :param url_args:    A dict of key/value pairs for GET parameters. E.g.,
                        {'language': 'en', }.
    :return: The complete admin url
    """
    base_url = admin_reverse(action, args=action_args)
    # Converts [{key: value}, …] => ["key=value", …]
    params = urlencode(url_args)
    if params:
        return "?".join([base_url, params])
    else:
        return base_url


@toolbar_pool.register
class FaqToolbar(CMSToolbar):
    watch_models = (Category, )
    config = None

    def __get_faq_config(self):
        try:
            __, config = get_app_instance(self.request)
            if not isinstance(config, FaqConfig):
                # This is not the app_hook you are looking for.
                return None
        except ImproperlyConfigured:
            # There is no app_hook at all.
            return None

        return config

    def get_category_list_url(self, lang=None):
        """
        Returns url for faq-category-list view with respect to lang or
        current_lang
        """
        with force_language(lang if lang else self.current_lang):
            url = reverse('{0}:faq-category-list'.format(
                self.config.namespace))
        return url

    def get_on_delete_redirect_url(self, obj, lang=None):
        if not self.config:
            self.config = self.__get_faq_config()

        if isinstance(obj, Category):
            url = self.get_category_list_url(lang)
        elif isinstance(obj, Question):
            category = obj.category
            lang = lang if lang else self.current_lang
            if category:
                url = category.get_absolute_url(language=lang)
            else:
                url = self.get_category_list_url(lang)
        return url

    def populate(self):
        self.config = self.__get_faq_config()
        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name and self.config:
            language = get_language_from_request(self.request, check_path=True)

            category = get_obj_from_request(Category, self.request,
                                            pk_url_kwarg='category_pk',
                                            slug_url_kwarg='category_slug')

            question = get_obj_from_request(Question, self.request)

            menu = self.toolbar.get_or_create_menu('faq-app',
                                                   self.config.get_app_title())

            change_config_perm = user.has_perm('aldryn_faq.change_faqconfig')
            config_perms = [change_config_perm, ]

            add_category_perm = user.has_perm('aldryn_faq.add_category')
            change_category_perm = user.has_perm('aldryn_faq.change_category')
            delete_category_perm = user.has_perm('aldryn_faq.delete_category')
            category_perms = [add_category_perm, change_category_perm,
                              delete_category_perm]

            add_question_perm = user.has_perm('aldryn_faq.add_question')
            change_question_perm = user.has_perm('aldryn_faq.change_question')
            delete_question_perm = user.has_perm('aldryn_faq.delete_question')
            question_perms = [add_question_perm, change_question_perm,
                              delete_question_perm]

            # ------ App Config items -----------------------------------------

            if change_config_perm:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('aldryn_faq_faqconfig_change',
                                    [self.config.pk, ], **url_args)
                menu.add_modal_item(_('Configure addon'), url=url)

            if any(config_perms) and any(category_perms + question_perms):
                menu.add_break()

            # ------ Category items -------------------------------------------

            if change_category_perm:
                url_args = {'appconfig__id__exact': self.config.pk}
                url = get_admin_url('aldryn_faq_category_changelist',
                                    **url_args)
                menu.add_sideframe_item(_('Category list'), url=url)

            if add_category_perm:
                url_args = {'appconfig': self.config.pk, }
                if language:
                    url_args.update({'language': language, })
                url = get_admin_url('aldryn_faq_category_add', **url_args)
                menu.add_modal_item(_('Add new category'), url=url)

            if change_category_perm and category:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('aldryn_faq_category_change',
                                    [category.pk, ], **url_args)
                menu.add_modal_item(_('Edit this category'), url=url,
                                    active=True)

            if delete_category_perm and category:
                redirect_url = self.get_on_delete_redirect_url(
                    category, language)
                url = get_admin_url('aldryn_faq_category_delete',
                                    [category.pk, ])
                menu.add_modal_item(_('Delete this category'), url=url,
                                    on_close=redirect_url)

            if any(config_perms + category_perms) and any(question_perms):
                menu.add_break()

            # ------ Question items -------------------------------------------

            if add_question_perm:
                url_args = {'appconfig': self.config.pk, }
                if language:
                    url_args.update({'language': language, })
                if category:
                    url_args.update({'category': category.pk, })
                url = get_admin_url('aldryn_faq_question_add', **url_args)
                menu.add_modal_item(_('Add new question'), url=url)

            if change_question_perm and question:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('aldryn_faq_question_change',
                                    [question.pk, ], **url_args)
                menu.add_modal_item(_('Edit this question'), url=url,
                                    active=True)

            if delete_question_perm and question:
                redirect_url = self.get_on_delete_redirect_url(
                    question, language)
                url = get_admin_url('aldryn_faq_question_delete',
                                    [question.pk, ])
                menu.add_modal_item(_('Delete this question'), url=url,
                                    on_close=redirect_url)
