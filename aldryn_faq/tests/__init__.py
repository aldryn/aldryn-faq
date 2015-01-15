# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model

# from cms.utils.i18n import get_language_list
from hvad.test_utils.context_managers import LanguageOverride

from aldryn_faq.models import Category, Question

User = get_user_model()


class AldrynFaqTestMixin(object):
    data = {
        "category1": {
            "en": {"name": "Example", "slug": "example", },
            "de": {"name": "Beispiel", "slug": "beispiel", }
        },
        "category2": {
            # This should *not* have a EN translation
            "de": {"name": "Beispiel2", "slug": "beispiel2", }
        },
        "question1": {
            "en": {"title": "Test Question", "answer_text": "Test Answer", },
            "de": {"title": "Testfrage", "answer_text": "Test Antwort"},
        },
        "question2": {
            # This should *not* have a EN translation
            "de": {"title": "Testfrage2", "answer_text": "Test Antwort2"},
        },
    }

    @staticmethod
    def reload(object):
        """Simple convenience method for re-fetching an object from the ORM."""
        return object.__class__.objects.get(id=object.id)

    def mktranslation(self, obj, lang, **kwargs):
        """Simple method of adding a translation to an existing object."""
        obj.translate(lang)
        for k, v in kwargs.iteritems():
            setattr(obj, k, v)
        obj.save()

    def setUp(self):
        """Setup a prebuilt and translated Question with Category
        for testing."""
        with LanguageOverride("en"):
            self.category1 = Category(**self.data["category1"]["en"])
            self.category1.save()
            self.question1 = Question(**self.data["question1"]["en"])
            self.question1.category = self.category1
            self.question1.save()

        # Make a DE translation of the category
        self.mktranslation(self.category1, "de",
            **self.data["category1"]["de"])
        # Make a DE translation of the question
        self.mktranslation(self.question1, "de",
            **self.data["question1"]["de"])

        with LanguageOverride("de"):
            # Make a DE-only Category
            self.category2 = Category(**self.data["category2"]["de"])
            self.category2.save()

            # Make a DE-only Question
            self.question2 = Question(**self.data["question2"]["de"])
            self.question2.category = self.category2
            self.question2.save()

    def assertListContentsEqual(self, a, b):
        """Tests that both lists contain the same element without regard to
        their order."""
        return self.assertEqual(
            sorted(a), sorted(b)
        )
