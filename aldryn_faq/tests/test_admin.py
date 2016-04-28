# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test.utils import override_settings
from cms.utils.urlutils import admin_reverse
from djangocms_helper.utils import create_user

from .test_base import AldrynFaqTest


# session engine is hardcoded in djangocms-helper (atm v0.9.4), so override
# per test case
@override_settings(SESSION_ENGINE='django.contrib.sessions.backends.cached_db')
class AdminViewsTestCase(AldrynFaqTest):
    tag_html = '<p>no html</p>'
    escaped_tag_html = '&lt;p&gt;no html&lt;/p&gt;'

    def setUp(self):
        super(AdminViewsTestCase, self).setUp()
        username = 'admin_user'
        password = 'test'
        self.admin_user = create_user(
            username=username,
            email='test@example.com',
            password=password,
            is_superuser=True,
        )
        self.client.login(username=username, password=password)

    def _test_admin_view(self, view_name, args=None):
        view_url = admin_reverse(view_name, args=args)
        response = self.client.get(view_url)
        # ensure that html was escaped
        self.assertNotContains(response, self.tag_html)
        self.assertContains(response, self.escaped_tag_html)

    def test_admin_add_veiw(self):
        view_name = 'aldryn_faq_question_change'
        self.question1.tags.add(self.tag_html)
        self._test_admin_view(view_name, args=[self.question1.pk])

    def test_admin_changelist_veiw(self):
        view_name = 'aldryn_faq_question_changelist'
        self.question1.tags.add(self.tag_html)
        self._test_admin_view(view_name)
