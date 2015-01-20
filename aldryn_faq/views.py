# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import resolve
from django.db import models
from django.shortcuts import get_list_or_404
from django.utils.translation import get_language_from_request
from django.views.generic import DetailView
from django.views.generic.list import ListView

from menus.utils import set_language_changer

from . import request_faq_category_identifier, request_faq_question_identifier
from .models import Category, Question


class FaqMixin(object):

    model = Question

    def dispatch(self, request, *args, **kwargs):
        self.current_language = get_language_from_request(
            self.request, check_path=True)
        return super(FaqMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FaqMixin, self).get_context_data(**kwargs)
        context['current_app'] = resolve(self.request.path).namespace
        return context

    def get_queryset(self):
        return self.model.objects.language(self.current_language)


class FaqByCategoryView(FaqMixin, ListView):

    template_name = 'aldryn_faq/questiontranslation_list.html'

    def get(self, *args, **kwargs):
        self.category = self.get_category()
        setattr(self.request, request_faq_category_identifier, self.category)
        response = super(FaqByCategoryView, self).get(*args, **kwargs)
        set_language_changer(self.request, self.category.get_absolute_url)
        return response

    def get_category(self):
        language = get_language_from_request(self.request)
        return Category.objects.active_translations(
            language, slug=self.kwargs['category_slug'])[0]

    def get_queryset(self):
        queryset = super(FaqByCategoryView, self).get_queryset()
        return queryset.filter(category=self.category).order_by('order')


class FaqAnswerView(FaqMixin, DetailView):

    template_name = 'aldryn_faq/question_detail.html'

    def get(self, *args, **kwargs):
        question = self.get_object()
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
