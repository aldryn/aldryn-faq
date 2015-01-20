# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import override, ugettext_lazy as _

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from cms.utils.i18n import get_current_language

from parler.models import TranslatableModel, TranslatedFields

from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable

from djangocms_text_ckeditor.fields import HTMLField

from sortedm2m.fields import SortedManyToManyField

from .managers import CategoryManager, RelatedManager


def get_translation(obj, lang):
    """This is an adapter from django-hvad.utils.get_translation(), a function
    to django-parler.models.get_translation() (a model instance method)."""
    return obj.get_translation(lang)


def get_slug_in_language(record, language):
    if not record:
        return None
    if not hasattr(record, "language_code"):
        return None
    if language == record.language_code:
        return record.lazy_translation_getter('slug')
    else:  # hit db
        try:
            translation = get_translation(record, language_code=language)
        except models.ObjectDoesNotExist:
            return None
        else:
            return translation.slug


@python_2_unicode_compatible
class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        slug=models.SlugField(verbose_name=_('Slug'), max_length=255),
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        if six.PY2:
            return self.lazy_translation_getter('name', unicode(self.pk))
        else:
            return self.lazy_translation_getter('name', str(self.pk))

    def model_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id

    def get_absolute_url(self, language=None):
        language = language or get_current_language()
        slug = get_slug_in_language(self, language)
        with override(language):
            if not slug:  # category not translated in given language
                return '/%s/' % language
            kwargs = {'category_slug': slug}
            return reverse('aldryn_faq:faq-category', kwargs=kwargs)


@python_2_unicode_compatible
class Question(TranslatableModel, Sortable):
    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255),
        answer_text=HTMLField(_('answer'))
    )
    category = SortableForeignKey(Category, related_name='questions')

    answer = PlaceholderField(
        'faq_question_answer', related_name='faq_questions')
    is_top = models.BooleanField(default=False)
    number_of_visits = models.PositiveIntegerField(default=0, editable=False)

    objects = RelatedManager()

    class Meta(Sortable.Meta):
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.lazy_translation_getter('title', str(self.pk))

    def model_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id

    def get_absolute_url(self, language=None):
        language = language or get_current_language()
        category = self.category
        try:
            translation = get_translation(self, language_code=language)
        except models.ObjectDoesNotExist:
            translation = None
        cat_slug = get_slug_in_language(category, language)
        if translation and cat_slug:
            with override(language):
                return reverse(
                    'aldryn_faq:faq-answer', args=(cat_slug, self.pk))
        else:
            return category.get_absolute_url(language)


class QuestionsPlugin(models.Model):
    questions = models.IntegerField(
        default=5,
        help_text=_('The number of questions to be displayed.')
    )

    def get_queryset(self):
        return Question.objects.filter_by_language(self.language)

    def get_questions(self):
        questions = self.get_queryset()
        return questions[:self.questions]

    class Meta:
        abstract = True


@python_2_unicode_compatible
class QuestionListPlugin(CMSPlugin):
    questions = SortedManyToManyField(Question)

    def __str__(self):
        return str(self.questions.count())

    def copy_relations(self, oldinstance):
        self.questions = oldinstance.questions.all()

    def get_questions(self):
        return self.questions.all()


class CategoryListPlugin(CMSPlugin):

    def copy_relations(self, oldinstance):
        for category in oldinstance.selected_categories.all():
            category.pk = None
            category.cms_plugin = self
            category.save()

    def get_categories(self):
        """
        By default, if no categories were chosen return all categories.
        Otherwise, return the chosen categories.
        """
        categories = Category.objects.get_categories(language=self.language)

        if self.selected_categories.exists():
            category_ids = self.selected_categories.values_list(
                'category__pk', flat=True)
            # categories is a list, and a sorted one so no need for another db
            # call.
            selected_categories = []
            for id in category_ids:
                category = next((x for x in categories if x.pk == id), None)
                if category:
                    selected_categories.append(category)
            return selected_categories
        return categories


class LatestQuestionsPlugin(CMSPlugin, QuestionsPlugin):

    def get_queryset(self):
        qs = super(LatestQuestionsPlugin, self).get_queryset()
        return qs.order_by('-id')


@python_2_unicode_compatible
class SelectedCategory(models.Model):
    category = models.ForeignKey(to=Category, verbose_name=_('category'))
    position = models.PositiveIntegerField(
        verbose_name=_('position'), blank=True, null=True)
    cms_plugin = models.ForeignKey(
        to=CategoryListPlugin, related_name='selected_categories')

    class Meta:
        ordering = ['position']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.category.name


class TopQuestionsPlugin(CMSPlugin, QuestionsPlugin):

    def get_queryset(self):
        qs = super(TopQuestionsPlugin, self).get_queryset()
        return qs.filter(is_top=True)


class MostReadQuestionsPlugin(CMSPlugin, QuestionsPlugin):

    def get_queryset(self):
        qs = super(MostReadQuestionsPlugin, self).get_queryset()
        return qs.order_by('-number_of_visits')
