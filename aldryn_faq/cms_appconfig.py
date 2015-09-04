# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.models import AppHookConfig
from aldryn_reversion.core import version_controlled_content
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields

# Different styles of slugs supported where 1 is the category PK and 2 is the
# question PK
PERMALINK_CHOICES = (
    ('Pp', _('1/2/', )),
    ('Ps', _('1/question-slug/', )),
    ('Sp', _('category-slug/2/', )),
    ('Ss', _('category-slug/question-slug/', )),  # Default
    ('Bp', _('1-category-slug/2/', )),
    ('Bs', _('1-category-slug/question-slug/', )),
)

NON_PERMALINK_HANDLING = (
    (200, _('Allow')),
    (302, _('Redirect to permalink (default)')),  # Default
    (301, _('Permanent redirect to permalink')),
    (404, _('Return 404: Not Found')),
)


@version_controlled_content()
class FaqConfig(TranslatableModel, AppHookConfig):
    """Adds some translatable, per-app-instance fields."""
    translations = TranslatedFields(
        app_title=models.CharField(_('application title'), max_length=234),
    )

    permalink_type = models.CharField(_('permalink type'), max_length=2,
        blank=False, choices=PERMALINK_CHOICES, default="Ss",
        help_text=_('Choose the style of urls to use from the examples. '
                    '(Note, all types are relative to apphook)'))

    non_permalink_handling = models.SmallIntegerField(
        _('non-permalink handling'),
        blank=False, default=302,
        choices=NON_PERMALINK_HANDLING,
        help_text=_('How to handle non-permalink urls?'))

    # Category List PHFs
    placeholder_faq_sidebar_top = PlaceholderField(
        'faq_sidebar_top', related_name='aldryn_faq_sidebar_top')

    placeholder_faq_sidebar_bottom = PlaceholderField(
        'faq_sidebar_bottom', related_name='aldryn_faq_sidebar_bottom')

    placeholder_faq_content = PlaceholderField(
        'faq_content', related_name='aldryn_faq_content')

    # Question list PHFs
    placeholder_faq_list_top = PlaceholderField(
        'faq_list_top', related_name='aldryn_faq_list_top')

    placeholder_faq_list_bottom = PlaceholderField(
        'faq_list_bottom', related_name='aldryn_faq_list_bottom')

    class Meta:
        verbose_name = 'config'
        verbose_name_plural = 'configs'

    def get_app_title(self):
        return getattr(self, 'app_title', _('untitled'))
