from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Page


class PageViewTestCase(TestCase):
    def setUp(self):
        super(PageViewTestCase, self).setUp()
        self.page = Page.objects.create(
            title='Racing Builds!',
            content="# Builds\n\n* MAEK U AN EAGLE\n* FLY IT"
        )

    def test_show_page(self):
        resp = self.client.get(reverse(
            'pages_show_page',
            kwargs={
                'slug': self.page.slug
            }
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['page'].title, self.page.title)

    def test_show_page_404(self):
        resp = self.client.get(reverse(
            'pages_show_page',
            kwargs={
                'slug': 'nopenopenope'
            }
        ))
        self.assertEqual(resp.status_code, 404)
