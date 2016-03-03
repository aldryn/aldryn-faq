# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve, reverse
from django.db import models
from django.http import (
    Http404,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.utils.translation import (
    get_language_from_request,
    override as force_language,
    ugettext,
)
from django.views.generic import DetailView
from django.views.generic.list import ListView

from aldryn_apphooks_config.mixins import AppConfigMixin
from parler.views import FallbackLanguageResolved, TranslatableSlugMixin
from parler.utils import get_active_language_choices
from menus.utils import set_language_changer

from .models import Category, Question

from . import request_faq_category_identifier, request_faq_question_identifier


# TODO: Move this to Aldryn Translation Tools
class AllowPKsTooMixin(object):
    def get_object(self, queryset=None):
        """
        Bypass TranslatableSlugMixin if we are using PKs. You would only use
        this if you have a obj that supports accessing the object by pk or
        by its translatable slug.

        NOTE: This should only be used on DetailViews and this mixin MUST be
        placed to the left of TranslatableSlugMixin. In fact, for best results,
        declare your obj like this:

            MyView(…, AllowPKsTooMixin, TranslatableSlugMixin, DetailView):
        """
        if self.pk_url_kwarg in self.kwargs:
            return super(DetailView, self).get_object(queryset)

        # OK, just let Parler have its way with it.
        return super(AllowPKsTooMixin, self).get_object(queryset)


# TODO: Move this to Aldryn Translation Tools
class CanonicalUrlMixin(object):
    """
    Provides configurable control over how non-canonical URLs to views are
    handled. A view can specify by setting 'non_canonical_url_response_type' to
    one of 200, 301, 302 or 404. By default, handling will be to temporarily
    redirect to the canonical URL.
    """
    non_canonical_url_response_type = 302

    def get_non_canonical_url_response_type(self):
        response_type = getattr(self, "non_canonical_url_response_type", None)
        if response_type and response_type in [200, 301, 302, 404]:
            return response_type
        else:
            return self.non_canonical_url_response_type

    def get(self, request, *args, **kwargs):
        """
        On GET, if the URL used is not the correct one, handle according to
        preferences by either:
            Allowing (200),
            Temporarily redirecting (302),
            Permanently redirecting (301) or
            Failing (404).
        """
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        url = self.object.get_absolute_url()
        response_type = self.get_non_canonical_url_response_type()
        if response_type == 200 or request.path == url:
            return super(CanonicalUrlMixin, self).get(
                request, *args, **kwargs)
        if response_type == 302:
            return HttpResponseRedirect(url)
        elif response_type == 301:
            return HttpResponsePermanentRedirect(url)
        else:
            raise Http404('This is not the canonical uri of this object.')


class FaqCategoryMixin(AppConfigMixin):
    """
    Provides support for getting the category from the URL, even if the view
    using it is a DetailView for a different model, or not a DetailView at all.
    """
    category_pk_url_kwarg = 'category_pk'
    category_slug_url_kwarg = 'category_slug'

    def dispatch(self, request, *args, **kwargs):
        self.current_language = get_language_from_request(
            request, check_path=True)
        return super(FaqCategoryMixin, self).dispatch(
            request, *args, **kwargs)

    def get_language_choices(self):
        """
        Define the language choices for the view, defaults to the defined
        settings.
        """
        return get_active_language_choices(self.current_language)

    def get_category(self, queryset=None):
        """
        Fetch the object using a translated slug. This is largely stolen from
        Parler, but modified to remove any assumptions that this is being used
        on a DetailView.
        """
        if queryset is None:
            queryset = self.get_category_queryset()

        slug = self.kwargs.get(self.category_slug_url_kwarg, None)
        pk = self.kwargs.get(self.category_pk_url_kwarg, None)
        choices = self.get_language_choices()

        error_message = ugettext(
            "No %(verbose_name)s found matching the query") % {
                'verbose_name': queryset.model._meta.verbose_name}

        if pk:
            try:
                obj = Category.objects.get(pk=pk)
            except ObjectDoesNotExist:
                raise Http404(error_message)
        elif slug:
            obj = None
            using_fallback = False
            prev_choices = []
            for lang_choice in choices:
                try:
                    # Get the single item from the filtered queryset
                    # NOTE. Explicitly set language to the state the object was
                    # fetched in.
                    filters = {'slug': slug}
                    obj = queryset.translated(
                        lang_choice, **filters).language(lang_choice).get()
                except ObjectDoesNotExist:
                    # Translated object not found, next object is marked as
                    # fallback.
                    using_fallback = True
                    prev_choices.append(lang_choice)
                else:
                    break

            if obj is None:
                tried_msg = ", tried languages: {0}".format(", ".join(choices))
                raise Http404(error_message + tried_msg)

            # Object found!
            if using_fallback:
                for prev_choice in prev_choices:
                    if obj.has_translation(prev_choice):
                        raise FallbackLanguageResolved(obj, prev_choice)

        else:
            raise Http404(error_message)

        return obj

    def get_category_queryset(self):
        return Category.objects.language(language_code=self.current_language)

    def handle_old_url_exception(self, error):
        return HttpResponsePermanentRedirect(error.new_url_format)


class FaqAnswerView(CanonicalUrlMixin, FaqCategoryMixin, AllowPKsTooMixin,
                    TranslatableSlugMixin, DetailView):
    template_name = 'aldryn_faq/question_detail.html'
    model = Question

    def get_non_canonical_url_response_type(self):
        if not hasattr(self, 'object'):
            self.object = self.get_object()

        try:
            return self.object.category.appconfig.non_permalink_handling
        except AttributeError:
            return super(
                FaqAnswerView, self).get_non_canonical_url_response_type()

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_category()
        except FallbackLanguageResolved as flr:
            # We have the category, but it is in a fallback language.
            category = flr.object

        # only look at questions within this category
        queryset = self.get_queryset().filter(category=category.pk)
        question = self.get_object(queryset=queryset)
        set_language_changer(request, question.get_absolute_url)

        if hasattr(request, 'toolbar'):
            request.toolbar.set_object(question)

        setattr(request, request_faq_category_identifier, question.category)
        setattr(request, request_faq_question_identifier, question)
        response = super(FaqAnswerView, self).get(request, *args, **kwargs)

        # FIXME: We should check for unique visitors using sessions.
        # update number of visits
        question_only_queryset = self.get_queryset().filter(pk=question.pk)
        question_only_queryset.update(
            number_of_visits=models.F('number_of_visits') + 1)
        return response

    def get_category_url(self):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        category = self.object.category
        return category.get_absolute_url(self.current_language)

    def get_context_data(self, **kwargs):
        context = super(FaqAnswerView, self).get_context_data(**kwargs)
        context['category_url'] = self.get_category_url()
        return context

    def get_object(self, queryset=None):
        if not hasattr(self, 'object'):
            # this is done because this method gets called twice.
            # so no need to query db twice.
            self.object = super(FaqAnswerView, self).get_object(queryset)
        return self.object

    def handle_old_url_exception(self, error):
        match = resolve(error.new_url_format)

        kwargs = match.kwargs
        kwargs['pk'] = self.kwargs['pk']
        url_name = '{0}:faq-answer'.format(match.namespace)

        with force_language(self.current_language):
            new_url_format = reverse(url_name, kwargs=kwargs)
        return HttpResponsePermanentRedirect(new_url_format)


class FaqByCategoryView(CanonicalUrlMixin, FaqCategoryMixin, ListView):
    template_name = 'aldryn_faq/question_list.html'
    model = Question

    def get_non_canonical_url_response_type(self):
        if not hasattr(self, 'object'):
            self.object = self.get_object()

        try:
            return self.object.appconfig.non_permalink_handling
        except AttributeError:
            return super(
                FaqByCategoryView, self).get_non_canonical_url_response_type()

    def get(self, request, *args, **kwargs):
        category = self.get_category()
        self.category = category

        setattr(request, request_faq_category_identifier, self.category)
        set_language_changer(request, self.category.get_absolute_url)
        response = super(FaqByCategoryView, self).get(request, *args, **kwargs)
        return response

    def get_object(self):
        return super(FaqByCategoryView, self).get_category()

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = (
            self.get_category_queryset().active_translations(
                self.current_language).filter(appconfig=self.config))
        kwargs['active_category'] = self.get_category()
        return super(FaqByCategoryView, self).get_context_data(**kwargs)

    def get_queryset(self):
        queryset = super(FaqByCategoryView, self).get_queryset()
        # get questions with fallbacks
        queryset = queryset.active_translations(self.current_language)
        # only matching current category
        queryset = queryset.filter(category=self.category).order_by('order')
        return queryset


class FaqQuestionMixin(AppConfigMixin):
    model = Question

    def dispatch(self, request, *args, **kwargs):
        """Determines the current language from the request, stores it."""
        self.current_language = get_language_from_request(
            request, check_path=True)
        return super(FaqQuestionMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FaqQuestionMixin, self).get_context_data(**kwargs)
        context['current_app'] = self.namespace
        return context

    def get_queryset(self):
        queryset = self.model.objects.language(
            language_code=self.current_language
        ).select_related('category')
        return queryset


class FaqByCategoryListView(FaqCategoryMixin, ListView):
    template_name = 'aldryn_faq/landing.html'
    model = Category

    def get_queryset(self):
        return self.model.objects.language(
            language_code=self.current_language).active_translations(
                self.current_language).filter(appconfig=self.config)
