# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

from hvad.forms import TranslatableModelForm

from sortedm2m.forms import SortedMultipleChoiceField

from .models import Category, QuestionListPlugin, Question


class CategoryAdminForm(TranslatableModelForm):

    class Meta:
        model = Category

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        translations_model = Category._meta.translations_model
        categories_with_slug = translations_model.objects.filter(slug=slug)

        if self.instance.pk:
            # Make sure to exclude references from this master :)
            categories_with_slug = categories_with_slug.exclude(
                master_id=self.instance.pk)

        if categories_with_slug.exists():
            raise forms.ValidationError(
                'A category with this slug already exists.')
        return slug


class QuestionListPluginForm(forms.ModelForm):

    questions = SortedMultipleChoiceField(queryset=Question.objects.none())

    class Meta:
        model = QuestionListPlugin

    def __init__(self, *args, **kwargs):
        super(QuestionListPluginForm, self).__init__(*args, **kwargs)
        questions_field = self.fields['questions']
        questions_field.queryset = Question.objects.language()
