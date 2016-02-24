# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import override, ugettext_lazy as _, ungettext

from aldryn_reversion.core import version_controlled_content
from aldryn_translation_tools.models import (
    TranslationHelperMixin, TranslatedAutoSlugifyMixin)
from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from cms.utils.i18n import get_current_language

from djangocms_text_ckeditor.fields import HTMLField
from parler.models import TranslatableModel, TranslatedFields
from sortedm2m.fields import SortedManyToManyField
from taggit.managers import TaggableManager

from .cms_appconfig import FaqConfig
from .managers import CategoryManager, RelatedManager
from .utils import is_valid_namespace, is_valid_app_config


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


def filter_question_qs(question_qs):
    """
    Filters provided question queryset to ensure that only apphooked
    namespaces are being used.
    :param question_qs: QuestionQueryset
    :return: filtered question_qs
    """
    app_configs = set()
    for question in question_qs.iterator():
        app_config = question.category.appconfig
        if (is_valid_app_config(app_config) and
                is_valid_namespace(app_config.namespace)):
            app_configs.add(app_config)
    return question_qs.filter(category__appconfig__in=app_configs)


@python_2_unicode_compatible
@version_controlled_content(follow=['appconfig'])
class Category(TranslatedAutoSlugifyMixin, TranslationHelperMixin,
               TranslatableModel):
    slug_source_field_name = 'name'

    translations = TranslatedFields(
        name=models.CharField(
            _('name'), max_length=255,
            help_text=_(u"Provide the category’s name")),
        slug=models.SlugField(
            verbose_name=_('Slug'), max_length=255, blank=True,
            help_text=_('Provide a "slug" for this category or leave blank for '
                        'an auto-generated one.')),
        description=HTMLField(
            verbose_name=_('description'), blank=True, default='',
            help_text=_('Optional. Description of this category.'))
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
        language = language or get_current_language()

        if not slug:
            slug = self.known_translation_getter(
                'slug', default=None, language_code=language)[0] or ''

        kwargs = {}
        try:
            permalink_type = self.appconfig.permalink_type
        except AttributeError:
            permalink_type = "Ss"

        if 'P' in permalink_type:
            kwargs.update({"category_pk": self.pk})
        elif 'S' in permalink_type:
            kwargs.update({"category_slug": slug})
        else:
            kwargs = {'category_pk': self.pk, 'category_slug': slug}

        if self.appconfig_id and self.appconfig.namespace:
            namespace = '{0}:'.format(self.appconfig.namespace)
        else:
            namespace = ''

        with override(language):
            return reverse('{0}faq-category'.format(namespace), kwargs=kwargs)


@python_2_unicode_compatible
@version_controlled_content(follow=['category'])
class Question(TranslatedAutoSlugifyMixin, TranslationHelperMixin,
               TranslatableModel):
    slug_source_field_name = 'title'

    translations = TranslatedFields(
        title=models.CharField(
            _('Title'), max_length=255,
            help_text=_(u"This should be a short form of the question")),
        answer_text=HTMLField(_('Short description')),
        slug=models.SlugField(
            verbose_name=_('Slug'), max_length=255, blank=True,
            help_text=_('Provide a "slug" for this category or leave blank for '
                        'an auto-generated one.')),
    )
    category = models.ForeignKey(Category, related_name='questions')

    answer = PlaceholderField(
        'faq_question_answer', related_name='faq_questions')
    is_top = models.BooleanField(default=False)
    number_of_visits = models.PositiveIntegerField(default=0, editable=False)

    tags = TaggableManager(blank=True)

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
        language = language or get_current_language()

        category_slug = self.category.known_translation_getter(
            'slug', default='', language_code=language)[0]

        question_slug = self.known_translation_getter(
            'slug', default='', language_code=language)[0]

        try:
            namespace = self.category.appconfig.namespace
        except AttributeError:
            namespace = False

        permalink_type = self.category.appconfig.permalink_type

        kwargs = {}
        if 'P' in permalink_type:
            kwargs.update({"category_pk": self.category.pk})
        elif 'S' in permalink_type:
            kwargs.update({"category_slug": category_slug})
        else:
            kwargs = {
                'category_pk': self.category.pk,
                'category_slug': category_slug
            }
        if 'p' in permalink_type:
            kwargs.update({"pk": self.pk})
        else:
            kwargs.update({"slug": question_slug})

        if namespace and category_slug:
            with override(language):
                url_name = '{0}:faq-answer'.format(namespace)
                return reverse(url_name, kwargs=kwargs)

        # No suitable translation exists, return the category's url
        return self.category.get_absolute_url(language)


class QuestionsPlugin(models.Model):
    questions = models.IntegerField(
        default=5,
        help_text=_('The number of questions to be displayed.')
    )

    def get_queryset(self):
        qs = filter_question_qs(
            Question.objects.filter_by_language(self.language))
        return qs

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
        qs = filter_question_qs(self.questions.all())
        return qs

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
        # ensure we don't try to resolve categories we cannot resolve
        categories = [
            category for category in Category.objects.get_categories(
                language=self.language)
            if is_valid_app_config(category.appconfig) and is_valid_namespace(
                category.appconfig.namespace)]

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
