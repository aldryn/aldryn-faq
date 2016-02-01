# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse

try:
    from reversion.revisions import create_revision, get_for_object
except ImportError:
    from reversion import create_revision, get_for_object

from django.db import transaction

from ..models import Category, Question, FaqConfig

from .test_base import AldrynFaqTest


class CommonAldrynReversionsAdminMixinTestCaseMixin(object):
    """
    Provides a set of utility methods and test cases to check if model was
    registered correctly with VersionnedPlaceholderAdminMixin from
    aldrun-reversions.
    The test is to perform reversing of recovery url if that is not failed with
    exception, models is considered to be registered correctly for django admin.

    Class attributes:
        model_class: class of a model to test against
        text_fields_to_change: list of text fields to change with random value
                               for generating reversion
        object_instance: instance of model_class which is already created and
                         can be used for tests.
    """
    model_class = None
    text_fields_to_change = []
    object_instance = None

    def setUp(self):
        super(CommonAldrynReversionsAdminMixinTestCaseMixin, self).setUp()
        self.create_revision_dummy()

    def create_revision_dummy(self):
        """
        Just create a revision with dummy data to ensure we have at least
        one revision.
        :return: None
        """
        object_instance = self.get_object_instance()
        for field in self.text_fields_to_change:
            setattr(object_instance, field, self.rand_str(prefix='dummy_'))
        with transaction.atomic():
            with create_revision():
                object_instance.save()

    def get_object_instance(self):
        """
        Should return model instance.
        Ensure that it returns model instance before using this mixin.
        Or set up self.object_instance during setUp method.
        """
        return self.object_instance

    def test_category_recovery_accessible(self):
        object_instance = self.get_object_instance()
        version = get_for_object(object_instance)[0]
        object_pk = object_instance.pk
        self.assertEqual(self.model_class.objects.filter(
            pk=object_pk).count(), 1)
        object_instance.delete()
        self.assertEqual(self.model_class.objects.filter(
            pk=object_pk).count(), 0)

        # check that there is a a way to access recovery view
        obj = version.object_version.object
        opts = obj._meta
        url = reverse(
            'admin:{0}_{1}_{2}'.format(
                opts.app_label,
                obj._meta.model_name,
                'recover'),
            args=[version.pk])
        # ust in case check the length, but at this step either a
        # NoReverseMatch should occur or other error,
        # if no exception is raised, it is a good sign
        self.assertGreater(len(url), 4)


class CategoryReversionAdminTestCase(
    CommonAldrynReversionsAdminMixinTestCaseMixin,
        AldrynFaqTest):

    model_class = Category
    text_fields_to_change = ['name', 'slug']

    def get_object_instance(self):
        return self.category1


class QuestionReversionAdminTestCase(
    CommonAldrynReversionsAdminMixinTestCaseMixin,
        AldrynFaqTest):

    model_class = Question
    text_fields_to_change = ['title', 'slug']

    def get_object_instance(self):
        return self.question1


class ConfigReversionAdminTestCase(
    CommonAldrynReversionsAdminMixinTestCaseMixin,
        AldrynFaqTest):

    model_class = FaqConfig
    text_fields_to_change = ['app_title']

    def get_object_instance(self):
        return self.app_config
