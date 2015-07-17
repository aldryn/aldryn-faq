# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import resolve, reverse
from django.db import models
from django.http import Http404, HttpResponsePermanentRedirect
from django.utils.translation import (
    get_language_from_request,
    override as force_language,
)
from django.views.generic import DetailView
from django.views.generic.list import ListView

from menus.utils import set_language_changer

from aldryn_apphooks_config.mixins import AppConfigMixin

from .models import Category, Question

from . import request_faq_category_identifier, request_faq_question_identifier
from .exceptions import OldCategoryFormatUsed
from .helpers import get_category_from_slug


class FaqMixin(AppConfigMixin):
    model = Question

    def dispatch(self, request, *args, **kwargs):
        self.current_language = get_language_from_request(
            request,
            check_path=True
        )
        return super(FaqMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FaqMixin, self).get_context_data(**kwargs)
        context['current_app'] = self.namespace
        return context

    def get_queryset(self):
        queryset = self.model.objects.language(
            language_code=self.current_language
        ).select_related('category')
        return queryset


class FaqCategoryMixin(FaqMixin):

    def dispatch(self, *args, **kwargs):
        try:
            return super(FaqCategoryMixin, self).dispatch(*args, **kwargs)
        except OldCategoryFormatUsed as error:
            return self.handle_old_url_exception(error)

    def get_category_or_404(self):
        """
        Looks for a category in the given slug.
        If none is found then raise a 404.
        """
        pk = self.kwargs.get('category_pk')
        slug = self.kwargs['category_slug']

        categories = Category.objects.filter(
            appconfig=self.config
        ).active_translations(self.current_language)

        category = get_category_from_slug(
            queryset=categories,
            slug=slug,
            pk=pk,
            language=self.current_language
        )

        if category is None:
            raise Http404("Category not found")
        return category

    def get_category_queryset(self):
        return Category.objects.filter(appconfig=self.config)

    def handle_old_url_exception(self, error):
        return HttpResponsePermanentRedirect(error.new_url_format)


class FaqByCategoryListView(FaqMixin, ListView):
    template_name = 'aldryn_faq/category_list.html'
    model = Category

    def get_queryset(self):
        qs = super(FaqByCategoryListView, self).get_queryset()
        return qs.filter(appconfig=self.config)


class FaqByCategoryView(FaqCategoryMixin, ListView):
    template_name = 'aldryn_faq/question_list.html'

    def get(self, request, *args, **kwargs):
        # triggers a redirect if the old category url format is used.
        category = self.get_category_or_404()
        category_url = category.get_absolute_url(self.current_language)

        if request.path != category_url:
            # say we have one category with two translations:
            # /en/faq/category-en/
            # /de/faq/category-de/
            # with this check we make sure that any request to
            # /en/faq/category-de/ gets redirected to /en/faq/category-en/
            return HttpResponsePermanentRedirect(category_url)

        self.category = category

        setattr(self.request, request_faq_category_identifier, self.category)
        set_language_changer(self.request, self.category.get_absolute_url)
        response = super(FaqByCategoryView, self).get(request, *args, **kwargs)
        return response

    def get_queryset(self):
        queryset = super(FaqByCategoryView, self).get_queryset()
        # get questions with fallbacks
        queryset = queryset.active_translations(self.current_language)
        # only matching current category
        queryset = queryset.filter(category=self.category).order_by('order')
        return queryset


class FaqAnswerView(FaqCategoryMixin, DetailView):
    template_name = 'aldryn_faq/question_detail.html'

    def get(self, request, *args, **kwargs):
        category = self.get_category_or_404()

        # only look at questions within this category
        queryset = self.get_queryset().filter(category=category.pk)

        question = self.get_object(queryset=queryset)
        question_url = question.get_absolute_url(self.current_language)

        if request.path != question_url:
            # say we have one category with two translations:
            # /en/faq/category-en/
            # /de/faq/category-de/
            # with this check we make sure that any request to
            # /en/faq/category-de/10/ gets redirected to /en/faq/category-en/10/
            # where 10 is the question id
            return HttpResponsePermanentRedirect(question_url)

        set_language_changer(self.request, question.get_absolute_url)

        if hasattr(self.request, 'toolbar'):
            self.request.toolbar.set_object(question)

        setattr(
            self.request, request_faq_category_identifier, question.category)

        setattr(self.request, request_faq_question_identifier, question)
        response = super(FaqAnswerView, self).get(request, *args, **kwargs)

        # FIXME: We should check for unique visitors using sessions.
        # update number of visits
        question_only_queryset = self.get_queryset().filter(pk=question.pk)
        question_only_queryset.update(
            number_of_visits=models.F('number_of_visits') + 1)
        return response

    def get_category_url(self):
        category = self.object.category
        return category.get_absolute_url(self.current_language)

    def get_context_data(self, **kwargs):
        context = super(FaqAnswerView, self).get_context_data(**kwargs)
        context['category_url'] = self.get_category_url()
        return context

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            # this is done because this method gets called twice.
            # so no need to query db twice.
            self._object = super(FaqAnswerView, self).get_object(queryset)
        return self._object

    def handle_old_url_exception(self, error):
        match = resolve(error.new_url_format)

        kwargs = match.kwargs
        kwargs['pk'] = self.kwargs['pk']
        url_name = '{0}:faq-answer'.format(match.namespace)

        with force_language(self.current_language):
            new_url_format = reverse(url_name, kwargs=kwargs)
        return HttpResponsePermanentRedirect(new_url_format)
