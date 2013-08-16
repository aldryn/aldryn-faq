from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable
from cms.models.fields import PlaceholderField
from django.conf import settings
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields


class RelatedManager(models.Manager):

    def filter_by_language(self, language):
        qs = self.get_query_set()
        return qs.filter(language=language)

    def filter_by_current_language(self):
        return self.filter_by_language(get_language())


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255)
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.lazy_translation_getter('name', str(self.pk))


class Question(Sortable):
    title = models.CharField(_('Title'), max_length=255)
    language = models.CharField(_('language'), max_length=5, choices=settings.LANGUAGES)
    category = SortableForeignKey(Category)
    answer = PlaceholderField('faq_question_answer', related_name='faq_questions')

    objects = RelatedManager()

    class Meta(Sortable.Meta):
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __unicode__(self):
        return self.title
