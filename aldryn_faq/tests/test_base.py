# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import RequestFactory, TransactionTestCase
from django.utils.translation import override

from cms import api
from cms.models import Title
from cms.utils import get_cms_setting
from cms.utils.i18n import get_language_list
from djangocms_helper.utils import create_user

from ..models import Category, Question, FaqConfig

User = get_user_model()


class TestUtilityMixin(object):
    """Just adds some common test utilities to the testing class."""
    def rand_str(self, prefix='', length=16, chars=string.ascii_letters):
        return prefix + ''.join(random.choice(chars) for _ in range(length))

    def assertEqualItems(self, a, b):
        try:
            # In Python3, this method has been renamed (poorly)
            assertCountEqual = self.assertCountEqual
        except AttributeError:
            # In 2.6, assertItemsEqual() doesn't sort first
            def assertCountEqual(a, b):
                return self.assertItemsEqual(sorted(a), sorted(b))

        return assertCountEqual(a, b)


class AldrynFaqTestMixin(TestUtilityMixin, object):
    """Sets up basic Category and Question objects for testing."""
    data = {
        "category1": {
            "en": {"name": "Example1", "slug": "example", },
            "de": {"name": "Beispiel1", "slug": "beispiel", }
        },
        "category2": {
            # This should *not* have a EN translation
            "de": {"name": "Beispiel2", "slug": "beispiel2", }
        },
        "question1": {
            "en": {"title": "Test Question", "answer_text": "Test Answer",
                   "slug": "test-question", },
            "de": {"title": "Testfrage", "answer_text": "Test Antwort",
                   "slug": "Testfrage", },
        },
        "question2": {
            # This should *not* have a EN translation
            "de": {"title": "Testfrage2", "answer_text": "Test Antwort2",
                   "slug": "testfrage2", },
        },
    }

    enabled_parler_fallback_settings = {
        'PARLER_LANGUAGES': {
            1: (
                {'code': 'de', 'fallbacks': ['en', ]},
                {'code': 'en', 'fallbacks': ['de', ]},
                {'code': 'fr', 'fallbacks': ['en', ]},
            ),
            'default': {
                'hide_untranslated': False,
            }
        }
    }

    disabled_parler_fallback_settings = {
        'PARLER_LANGUAGES': {
            1: (
                {'code': 'de'},
                {'code': 'en'},
                {'code': 'fr'},
            ),
            'default': {
                'hide_untranslated': False,
            }
        }
    }

    settings_en = {
        'LANGUAGES': (
            ('en', 'English'),
        ),
        'LANGUAGE': 'en',
        'PARLER_LANGUAGES': {
            1: (
                {'code': 'en'},
            ),
            'default': {
                'hide_untranslated': False,
            },
        },
        'CMS_LANGUAGES': {
            1: (
                {'code': 'en', 'name': 'English'},
            ),
            'default': {
                'hide_untranslated': False,
            },
        },
    }

    @staticmethod
    def reload(obj, language=None):
        """Simple convenience method for re-fetching an object from the ORM,
        optionally "as" a specified language."""
        if language:
            with override(language):
                new_obj = obj.__class__.objects.get(id=obj.id)
        else:
            new_obj = obj.__class__.objects.get(id=obj.id)
        return new_obj

    def mktranslation(self, obj, lang, **kwargs):
        """Simple method of adding a translation to an existing object."""
        obj.set_current_language(lang)
        for k, v in kwargs.items():
            setattr(obj, k, v)
        obj.save()

    def setUp(self):
        """Setup a prebuilt and translated Question with Category
        for testing."""
        super(AldrynFaqTestMixin, self).setUp()
        with override("en"):
            self.category1 = Category(**self.data["category1"]["en"])
            self.category1.appconfig = self.app_config
            self.category1.save()
            self.question1 = Question(**self.data["question1"]["en"])
            self.question1.category = self.category1
            self.question1.save()

        # Make a DE translation of the category
        self.mktranslation(
            self.category1,
            "de",
            **self.data["category1"]["de"]
        )

        # Make a DE translation of the question
        self.mktranslation(
            self.question1,
            "de",
            **self.data["question1"]["de"]
        )

        with override("de"):
            # Make a DE-only Category
            self.category2 = Category(**self.data["category2"]["de"])
            self.category2.appconfig = self.app_config
            self.category2.save()

            # Make a DE-only Question
            self.question2 = Question(**self.data["question2"]["de"])
            self.question2.category = self.category2
            self.question2.save()


class CMSRequestBasedTest(TestUtilityMixin, TransactionTestCase):
    """Sets-up User(s) and CMS Pages for testing."""
    languages = get_language_list()

    @classmethod
    def setUpClass(cls):
        cls.request_factory = RequestFactory()
        if not User.objects.filter(username='normal').count():
            cls.user = create_user('normal', 'normal@admin.com', 'normal')
        cls.site1 = Site.objects.get(pk=1)

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def setUp(self):
        super(CMSRequestBasedTest, self).setUp()
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.root_page = api.create_page(
            'root page',
            self.template,
            self.language,
            published=True
        )
        self.app_config = FaqConfig.objects.create(namespace='aldryn_faq',
                                                   permalink_type='Bp',
                                                   non_permalink_handling=301)
        self.page = api.create_page(
            'faq',
            self.template,
            self.language,
            published=True,
            parent=self.root_page,
            apphook='FaqApp',
            apphook_namespace=self.app_config.namespace
        )
        self.placeholder = self.page.placeholders.all()[0]

        for page in [self.root_page, self.page]:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, page.get_slug(), page)
                page.publish(language)

    def get_or_create_page(self, base_title=None, languages=None):
        """Creates a page with a given title, or, if it already exists, just
        retrieves and returns it."""
        from cms.api import create_page, create_title
        if not base_title:
            # No title? Create one.
            base_title = self.rand_str(prefix="page", length=8)
        if not languages:
            # If no langs supplied, use'em all
            languages = self.languages
        # If there is already a page with this title, just return it.
        try:
            page_title = Title.objects.get(title=base_title)
            return page_title.page.get_draft_object()
        except:
            pass

        # No? Okay, create one.
        page = create_page(base_title, 'fullwidth.html', language=languages[0])
        # If there are multiple languages, create the translations
        if len(languages) > 1:
            for lang in languages[1:]:
                title_lang = "{0}-{1}".format(base_title, lang)
                create_title(language=lang, title=title_lang, page=page)
                page.publish(lang)
        return page.get_draft_object()

    def get_page_request(
            self, page, user, path=None, edit=False, lang_code='en'):
        from cms.middleware.toolbar import ToolbarMiddleware
        path = path or page and page.get_absolute_url()
        if edit:
            path += '?edit'
        request = RequestFactory().get(path)
        request.session = {}
        request.user = user
        request.LANGUAGE_CODE = lang_code
        if edit:
            request.GET = {'edit': None}
        else:
            request.GET = {'edit_off': None}
        request.current_page = page
        mid = ToolbarMiddleware()
        mid.process_request(request)
        return request


class AldrynFaqTest(AldrynFaqTestMixin, CMSRequestBasedTest):
    pass
