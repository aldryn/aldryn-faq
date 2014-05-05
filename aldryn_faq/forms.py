from django import forms
from django.db.models.query import QuerySet

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
            categories_with_slug = categories_with_slug.exclude(master_id=self.instance.pk)

        if categories_with_slug.exists():
            raise forms.ValidationError('A category with this slug already exists.')
        return slug


class HvadFriendlySortedMultipleChoiceField(SortedMultipleChoiceField):

    def clean(self, value):
        '''Hvad doesn't implement in_bulk method but clean depends on it'''
        queryset = super(SortedMultipleChoiceField, self).clean(value)
        if value is None or not isinstance(queryset, QuerySet):
            return queryset
        queryset = queryset.filter(id__in=value)
        # sort questions with order in value list
        return sorted(queryset, key=lambda question: value.index(str(question.pk)))


class QuestionListPluginForm(forms.ModelForm):

    questions = HvadFriendlySortedMultipleChoiceField(queryset=Question.objects.none())

    class Meta:
        model = QuestionListPlugin

    def __init__(self, *args, **kwargs):
        super(QuestionListPluginForm, self).__init__(*args, **kwargs)
        questions_field = self.fields['questions']
        questions_field.queryset = Question.objects.language()
