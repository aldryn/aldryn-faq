# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import override, ugettext_lazy as _, ungettext

from aldryn_reversion.core import version_controlled_content
from aldryn_translation_tools.models import TranslationHelperMixin

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from cms.utils.i18n import get_current_language

from djangocms_text_ckeditor.fields import HTMLField
from parler.models import TranslatableModel, TranslatedFields
from sortedm2m.fields import SortedManyToManyField

from .cms_appconfig import FaqConfig
from .managers import CategoryManager, RelatedManager


def get_translation(obj, language_code):
    """
    This is an adapter from django-hvad.utils.get_translation(), a function
    to django-parler.models.get_translation() (a model instance method).
    """
    if not obj or not hasattr(obj, "get_translation"):
        return None
    return obj.get_translation(language_code)


def get_slug_in_language(record, language):
    """This is an adapter from django-hvad's lazy_translation_getter."""
    if not record or not hasattr(record, "safe_translation_getter"):
        return None
    return record.safe_translation_getter(
        field="slug", language_code=language, default=None, )


@python_2_unicode_compatible
@version_controlled_content
class Category(TranslationHelperMixin, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        slug=models.SlugField(verbose_name=_('Slug'), max_length=255),
    )
    appconfig = models.ForeignKey(
        FaqConfig, verbose_name=_('appconfig'), blank=True, null=True
    )
    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        pkstr = str(self.pk)
        if six.PY2:
            pkstr = six.u(pkstr)
        return self.safe_translation_getter('name', default=pkstr)

    def model_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id

    def get_absolute_url(self, language=None, slug=None):
        if language is None:
            language = get_current_language()

        if slug is None:
            slug = self.known_translation_getter(
                'slug',
                default=None,
                language_code=language
            )[0] or ''

        kwargs = {'category_pk': self.pk, 'category_slug': slug}

        if self.appconfig_id and self.appconfig.namespace:
            namespace = '{0}:'.format(self.appconfig.namespace)
        else:
            namespace = ''

        with override(language):
            return reverse('{0}faq-category'.format(namespace), kwargs=kwargs)


@python_2_unicode_compatible
@version_controlled_content
class Question(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255),
        answer_text=HTMLField(_('Short description'))
    )
    category = models.ForeignKey(Category, related_name='questions')

    answer = PlaceholderField(
        'faq_question_answer', related_name='faq_questions')
    is_top = models.BooleanField(default=False)
    number_of_visits = models.PositiveIntegerField(default=0, editable=False)

    objects = RelatedManager()

    order = models.PositiveIntegerField(default=1, db_index=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ('order', )

    def __str__(self):
        pkstr = str(self.pk)
        if six.PY2:
            pkstr = six.u(pkstr)
        return self.safe_translation_getter('title', default=pkstr)

    def model_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id

    def get_absolute_url(self, language=None):
        """
        Returns the absolute_url of this question object, respecting the
        configured fallback languages.
        """
        if language is None:
            language = get_current_language()

        category_slug = self.category.known_translation_getter(
            'slug',
            default=None,
            language_code=language
        )[0] or ''

        try:
            namespace = self.category.appconfig.namespace
        except:
            namespace = False

        if namespace and category_slug:
            with override(language):
                url_name = '{0}:faq-answer'.format(namespace)
                url_kwargs = {
                    'pk': self.pk,
                    'category_pk': self.category.pk,
                    'category_slug': category_slug,
                }
                return reverse(url_name, kwargs=url_kwargs)

        # No suitable translations exist, return the category's url
        return self.category.get_absolute_url(language)


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

    def copy_relations(self, oldinstance):
        self.questions = oldinstance.questions.all()

    def get_questions(self):
        return self.questions.all()

    def __str__(self):
        question_count = self.questions.count()
        return ungettext(
            "%(count)d question selected",
            "%(count)d questions selected",
            question_count
        ) % {"count": question_count, }


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
        verbose_name=_('position'), blank=True, default=0, null=True)
    cms_plugin = models.ForeignKey(
        to=CategoryListPlugin, related_name='selected_categories')

    class Meta:
        ordering = ['position', ]
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
