# -*- coding: utf-8 -*-
from django.views.generic.list import ListView

from . import models


class FAQView(ListView):

    def get_queryset(self):
        return models.Question.objects.filter_by_current_language()
