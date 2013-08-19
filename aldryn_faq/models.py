from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable
from aldryn_news.models import get_page_url
from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from cms.utils.i18n import get_current_language, force_language
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _
from hvad.manager import TranslationManager
from hvad.models import TranslatableModel, TranslatedFields
from hvad.utils import get_translation


def get_slug_in_language(record, language):
    if not record:
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


class RelatedManager(models.Manager):

    def filter_by_language(self, language):
        qs = self.get_query_set()
        return qs.filter(language=language)

    def filter_by_current_language(self):
        return self.filter_by_language(get_language())


class CategoryManager(TranslationManager):

    def get_categories(self, language):
        categories = self.language(language).prefetch_related('questions')

        for category in categories:
            category.count = (category.questions
                              .filter_by_language(language).count())
        return sorted(categories, key=lambda x: -x.count)


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        slug=models.SlugField(_('Slug'), max_length=255, blank=True,
                              help_text=_('Auto-generated. Clean it to have it re-created. '
                                          'WARNING! Used in the URL. If changed, the URL will change. ')),
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.lazy_translation_getter('name', str(self.pk))

    def get_absolute_url(self, language=None):
        language = language or get_current_language()
        slug = get_slug_in_language(self, language)
        with force_language(language):
            if not slug:  # category not translated in given language
                return get_page_url('faq', language)
            kwargs = {'category_slug': slug}
            return reverse('aldryn_faq:faq-category', kwargs=kwargs)


class Question(Sortable):
    title = models.CharField(_('Title'), max_length=255)
    language = models.CharField(_('language'), max_length=5, choices=settings.LANGUAGES)
    category = SortableForeignKey(Category, related_name='questions')
    answer = PlaceholderField('faq_question_answer', related_name='faq_questions')

    objects = RelatedManager()

    class Meta(Sortable.Meta):
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __unicode__(self):
        return self.title


class LatestQuestionPlugin(CMSPlugin):

    latest_questions = models.IntegerField(default=5, help_text=_('The number of latests questions to be displayed.'))

    def get_questions(self):
        questions = (Question.objects.filter_by_language(self.language)
                     .order_by('-id'))
        return questions[:self.latest_questions]
