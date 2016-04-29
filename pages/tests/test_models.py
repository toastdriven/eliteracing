from django.test import TestCase

from ..models import Page


class PageTestCase(TestCase):
    def test_save(self):
        # We need to ensure the `slug` & `content_html` get autopopulated here.
        page = Page.objects.create(
            title='Racing Builds!',
            content="# Builds\n\n* MAEK U AN EAGLE\n* FLY IT"
        )
        self.assertEqual(page.slug, 'racing-builds')
        self.assertEqual(
            page.content_html, 
            '<h1>Builds</h1>\n<ul>\n<li>MAEK U AN EAGLE</li>\n<li>FLY IT</li>\n</ul>'
        )
