# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.list import ListView
from menus.utils import set_language_changer

from . import models, request_faq_category_identifier, request_faq_question_identifier


class FaqByCategoryView(ListView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        setattr(self.request, request_faq_category_identifier, self.object)
        response = super(FaqByCategoryView, self).get(*args, **kwargs)
        set_language_changer(self.request, self.object.get_absolute_url)
        return response

    def get_object(self):
        return get_object_or_404(models.Category.objects.language(),
                                 slug=self.kwargs['category_slug'])

    def get_queryset(self):
        return (models.Question.objects
        .filter_by_current_language().filter(category=self.object)).order_by('order')


class FaqAnswerView(DetailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if hasattr(self.request, 'toolbar'):
            self.request.toolbar.set_object(self.object)
        setattr(self.request, request_faq_category_identifier, self.object.category)
        setattr(self.request, request_faq_question_identifier, self.object)
        response = super(FaqAnswerView, self).get(*args, **kwargs)
        return response

    def get_object(self):
        return get_object_or_404(models.Question, pk=self.kwargs['id'])

    def get_queryset(self):
        return (models.Question.objects
        .filter_by_current_language().filter(category=self.object))
