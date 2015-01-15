# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from hvad.test_utils.context_managers import LanguageOverride
from aldryn_faq.models import Category, Question


EN_CAT_NAME = "Example"
EN_CAT_SLUG = "example"
EN_QUE_TITLE = "Test Question"
EN_QUE_ANSWER_TEXT = "Test Answer"

DE_CAT_NAME = "Beispiel"
DE_CAT_SLUG = "beispiel"

# This should NOT have a EN translation
DE_CAT_NAME2 = "Beispiel2"
DE_CAT_SLUG2 = "beispiel2"

DE_QUE_TITLE = "Testfrage"
DE_QUE_ANSWER_TEXT = "Test Antwort"

# This should NOT have a EN translation
DE_QUE_TITLE2 = "Testfrage2"
DE_QUE_ANSWER_TEXT2 = "Test Antwort2"


class AldrynFaqTestMixin(object):

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
            self.category = Category(**{
                "name": EN_CAT_NAME,
                "slug": EN_CAT_SLUG
            })
            self.category.save()
            self.question = Question(**{
                "title": EN_QUE_TITLE,
                "answer_text": EN_QUE_ANSWER_TEXT,
            })
            self.question.category = self.category
            self.question.save()

        # Make a DE translation of the category
        self.mktranslation(self.category, "de", **{
            "name": DE_CAT_NAME,
            "slug": DE_CAT_SLUG,
        })
        # Make a DE translation of the question
        self.mktranslation(self.question, "de", **{
            "title": DE_QUE_TITLE,
            "answer_text": DE_QUE_ANSWER_TEXT,
        })

        with LanguageOverride("de"):
            # Make a DE-only Category
            self.category2 = Category(**{
                "name": DE_CAT_NAME2,
                "slug": DE_CAT_SLUG2
            })
            self.category2.save()

            # Make a DE-only Question
            self.question2 = Question(**{
                "title": DE_QUE_TITLE2,
                "answer_text": DE_QUE_ANSWER_TEXT2,
            })
            self.question2.category = self.category2
            self.question2.save()

    def assertListContentsEqual(self, a, b):
        """Tests that both lists contain the same element without regard to
        their order"""
        return self.assertEqual(
            sorted(a), sorted(b)
        )
