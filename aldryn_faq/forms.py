from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, get_language
from django import forms
from hvad.forms import TranslatableModelForm
from unidecode import unidecode
from sortedm2m.forms import SortedMultipleChoiceField

from .models import QuestionListPlugin, Question


class AutoSlugForm(TranslatableModelForm):

    slug_field = 'slug'
    slugified_field = None

    def clean(self):
        super(AutoSlugForm, self).clean()

        if not self.data.get(self.slug_field):
            slug = self.generate_slug()
            # add to self.data in order to show generated slug in the form in case of an error
            self.data[self.slug_field] = self.cleaned_data[self.slug_field] = slug
        else:
            slug = self.cleaned_data[self.slug_field]

        # validate uniqueness
        conflict = self.get_slug_conflict(slug=slug)
        if conflict:
            self.report_error(conflict=conflict)

        return self.cleaned_data

    def generate_slug(self):
        content_to_slugify = self.cleaned_data.get(self.slugified_field, '')
        return slugify(unidecode(content_to_slugify))

    def get_slug_conflict(self, slug):
        translations_model = self.instance._meta.translations_model

        try:
            language_code = self.instance.language_code
        except translations_model.DoesNotExist:
            language_code = get_language()

        conflicts = translations_model.objects.filter(slug=slug, language_code=language_code)
        if self.is_edit_action():
            conflicts = conflicts.exclude(master=self.instance)

        try:
            return conflicts.get()
        except translations_model.DoesNotExist:
            return None

    def report_error(self, conflict):
        address = '<a href="%(url)s" target="_blank">%(label)s</a>' % {
            'url': conflict.master.get_absolute_url(),
            'label': ugettext('the conflicting object')}
        error_message = ugettext('Conflicting slug. See %(address)s.') % {'address': address}
        self.append_to_errors(field='slug', message=mark_safe(error_message))

    def append_to_errors(self, field, message):
        try:
            self._errors[field].append(message)
        except KeyError:
            self._errors[field] = self.error_class([message])

    def is_edit_action(self):
        return self.instance.pk is not None


class CategoryForm(AutoSlugForm):

    slugified_field = 'name'

    class Meta:
        fields = ['name', 'slug']


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
