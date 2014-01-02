from aldryn_search.base import AldrynIndexBase
from aldryn_search.utils import strip_tags
from django.template import RequestContext
from haystack import indexes

from .models import Question


class QuestionIndex(AldrynIndexBase, indexes.Indexable):

    INDEX_TITLE = True

    def get_title(self, obj):
        return obj.title

    def get_index_kwargs(self, language):
        return {'language': language}

    def get_index_queryset(self, language):
        return self.get_model().objects.all()

    def get_model(self):
        return Question

    def get_search_data(self, obj, language, request):
        text = strip_tags(obj.title)
        text += u' ' + strip_tags(obj.answer_text)
        plugins = obj.answer.cmsplugin_set.filter(language=language)
        for base_plugin in plugins:
            instance, plugin_type = base_plugin.get_plugin_instance()
            if instance is None:
                # this is an empty plugin
                continue
            else:
                text += strip_tags(instance.render_plugin(context=RequestContext(request))) + u' '
        return text
