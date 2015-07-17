# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.http import Http404
from django.utils.translation import get_language_from_request
from django.views.generic import DetailView
from django.views.generic.list import ListView

from menus.utils import set_language_changer

from parler.views import TranslatableSlugMixin

from aldryn_apphooks_config.mixins import AppConfigMixin

from .models import Category, Question

from . import request_faq_category_identifier, request_faq_question_identifier


class FaqMixin(AppConfigMixin):
    model = Question

    def dispatch(self, request, *args, **kwargs):
        self.current_language = get_language_from_request(
            self.request, check_path=True)
        return super(FaqMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FaqMixin, self).get_context_data(**kwargs)
        context['current_app'] = self.namespace
        return context

    def get_category_or_404(self, slug, language):
        """
        Looks for a category with the given slug IN THE GIVEN LANGUAGE. This
        should not use fallbacks, otherwise it may be possible that we get the
        wrong category.
        """
        categories = Category.objects.filter(
            appconfig=self.config
        ).active_translations(language, slug=slug)

        if not categories:
            raise Http404("Category not found")
        return categories[0]

    def get_category_queryset(self):
        return Category.objects.filter(appconfig=self.config)

    def get_queryset(self):
        return self.model.objects.language(self.current_language)


class FaqByCategoryListView(FaqMixin, AppConfigMixin, ListView):
    template_name = 'aldryn_faq/category_list.html'
    model = Category

    def get_queryset(self):
        qs = super(FaqByCategoryListView, self).get_queryset()
        return qs.filter(appconfig=self.config)


class FaqByCategoryView(FaqMixin, TranslatableSlugMixin, ListView):
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'
    template_name = 'aldryn_faq/question_list.html'

    def get(self, *args, **kwargs):
        categories = self.get_category_queryset()
        category_pk = kwargs.get('category_pk')

        if category_pk:
            categories = categories.filter(pk=category_pk)

        self.category = self.get_object(queryset=categories)
        setattr(self.request, request_faq_category_identifier, self.category)
        set_language_changer(self.request, self.category.get_absolute_url)
        response = super(FaqByCategoryView, self).get(*args, **kwargs)
        return response

    def get_slug_field(self):
        return self.slug_field

    def get_queryset(self):
        queryset = super(FaqByCategoryView, self).get_queryset()
        queryset = queryset.active_translations(self.current_language)
        queryset = queryset.filter(category=self.category).order_by('order')
        return queryset


class FaqAnswerView(FaqMixin, DetailView):
    template_name = 'aldryn_faq/question_detail.html'

    def get(self, *args, **kwargs):
        category = self.get_category_or_404(
            slug=kwargs['category_slug'],
            language=self.current_language
        )

        question = self.get_object()

        if question.category_id != category.pk:
            raise Http404

        set_language_changer(self.request, question.get_absolute_url)

        if hasattr(self.request, 'toolbar'):
            self.request.toolbar.set_object(question)

        setattr(
            self.request, request_faq_category_identifier, question.category)

        setattr(self.request, request_faq_question_identifier, question)
        response = super(FaqAnswerView, self).get(*args, **kwargs)

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
            self._object = super(FaqAnswerView, self).get_object(queryset)
        return self._object
