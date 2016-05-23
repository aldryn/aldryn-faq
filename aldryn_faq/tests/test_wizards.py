# -*- coding: utf-8 -*-
from djangocms_helper.utils import create_user

from aldryn_faq.cms_wizards import CreateFaqQuestionForm

from .test_base import AldrynFaqTest


class TestFAQWizard(AldrynFaqTest):

    def setUp(self):
        super(TestFAQWizard, self).setUp()
        username = 'admin_user'
        password = 'test'
        self.admin_user = create_user(
            username=username,
            email='test@example.com',
            password=password,
            is_superuser=True,
        )
        self.client.login(username=username, password=password)

    def test_question_wizard(self):
        data = {
            'title': 'Where are we?',
            'answer': 'Here.',
            'answer_text': '<p>Interesting question..</p>',
            'category': self.category1.pk,
        }
        form = CreateFaqQuestionForm(
            data=data,
            wizard_language='en',
            wizard_user=self.admin_user,
        )
        self.assertTrue(form.is_valid())
        question = form.save()

        url = question.get_absolute_url('en')
        response = self.client.get(url)
        self.assertContains(response, 'Where are we?', status_code=200)
        self.assertContains(response, 'Here.', status_code=200)
