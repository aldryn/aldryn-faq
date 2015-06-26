# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.models import AppHookConfig
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields


class FaqConfig(TranslatableModel, AppHookConfig):
    """Adds some translatable, per-app-instance fields."""
    translations = TranslatedFields(
        app_title=models.CharField(_('application title'), max_length=234),
    )

    # Category List PHFs
    placeholder_faq_sidebar_top = PlaceholderField(
        'faq_sidebar_top', related_name='aldryn_faq_sidebar_top')

    placholder_faq_sidebar_bottom = PlaceholderField(
        'faq_sidebar_bottom', related_name='aldryn_faq_sidebar_bottom')

    placholder_faq_content = PlaceholderField(
        'faq_content', related_name='aldryn_faq_content')

    # Question list PHFs
    placholder_faq_list_top = PlaceholderField(
        'faq_list_top', related_name='aldryn_faq_list_top')

    placholder_faq_list_bottom = PlaceholderField(
        'faq_list_bottom', related_name='aldryn_faq_list_bottom')
