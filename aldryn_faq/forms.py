# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

from aldryn_apphooks_config.utils import setup_config
from app_data import AppDataForm
from parler.forms import TranslatableModelForm
from sortedm2m.forms import SortedMultipleChoiceField

from .models import Category, QuestionListPlugin, Question, FaqConfig


class CategoryAdminForm(TranslatableModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'appconfig',
        ]

    # def clean_slug(self):
    #     slug = self.cleaned_data['slug']
    #     translations_model = Category._meta.translations_model
    #     categories_with_slug = translations_model.objects.filter(slug=slug)

    #     if self.instance.pk:
    #         # Make sure to exclude references from this master :)
    #         categories_with_slug = categories_with_slug.exclude(
    #             master_id=self.instance.pk)

    #     if categories_with_slug.exists():
    #         raise forms.ValidationError(
    #             'A category with this slug already exists.')
    #     return slug


class QuestionListPluginForm(forms.ModelForm):

    questions = SortedMultipleChoiceField(queryset=Question.objects.none())

    class Meta:
        model = QuestionListPlugin
        fields = [
            'questions',
        ]

    def __init__(self, *args, **kwargs):
        super(QuestionListPluginForm, self).__init__(*args, **kwargs)
        questions_field = self.fields['questions']
        questions_field.queryset = Question.objects.language()


class FaqOptionForm(AppDataForm):
    show_description = forms.BooleanField(
        required=False,
        help_text=(
            "This option enables the short descirption to be available "
            "within the list view rendering for all plugins."
        )
    )

setup_config(FaqOptionForm, FaqConfig)
