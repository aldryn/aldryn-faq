# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.template import RequestContext

from aldryn_search.utils import get_index_base, strip_tags
from parler.utils.context import switch_language
from .models import Question, Category


class QuestionIndex(get_index_base()):

    haystack_use_for_indexing = getattr(
        settings, "ALDRYN_FAQ_QUESTION_SEARCH", True)

    index_title = True

    def get_title(self, obj):
        with switch_language(obj):
            return obj.safe_translation_getter('title')

    def get_index_queryset(self, language):
        questions = self.get_model().objects.language(language)
        return questions.active_translations(language)

    def get_model(self):
        return Question

    def get_search_data(self, obj, language, request):
        with switch_language(obj, language):
            context = RequestContext(request)
            text_bits = [
                strip_tags(obj.safe_translation_getter('title') or ''),
                strip_tags(obj.safe_translation_getter('answer_text') or '')
            ]
            plugins = obj.answer.cmsplugin_set.filter(language=language)
            for base_plugin in plugins:
                instance, plugin_type = base_plugin.get_plugin_instance()
                if instance is not None:
                    plugin_content = strip_tags(
                        instance.render_plugin(context=context)
                    )
                    text_bits.append(plugin_content)

            return ' '.join(text_bits)


class CategoryIndex(get_index_base()):

    haystack_use_for_indexing = getattr(
        settings, "ALDRYN_FAQ_CATEGORY_SEARCH", True)

    index_title = True

    def get_title(self, obj):
        with switch_language(obj):
            return obj.safe_translation_getter('name')

    def get_index_queryset(self, language):
        categories = self.get_model().objects.language(language)
        return categories.active_translations(language)

    def get_model(self):
        return Category

    def get_search_data(self, obj, language, request):
        with switch_language(obj):
            return strip_tags(obj.safe_translation_getter('name'))
