import mock
import os

from django.core.urlresolvers import reverse
from django.test import TestCase


class TestDocsViews(TestCase):
    def test_list(self):
        resp = self.client.get(reverse('docs_list'))
        self.assertEqual(resp.status_code, 200)

    def test_api_v1_courses(self):
        resp = self.client.get(reverse('docs_api_v1_courses'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['title'], 'API v1 - Courses')

    def test_not_found(self):
        with mock.patch.object(os.path, 'exists', return_value=False):
            resp = self.client.get(reverse('docs_api_v1_courses'))
            self.assertEqual(resp.status_code, 404)
