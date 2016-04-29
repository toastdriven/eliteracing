from django.contrib.auth.models import User
from django.test import TestCase

from ..models import NewsPost


class NewsPostTestCase(TestCase):
    def test_save(self):
        admin_user = User.objects.create_user(
            'admin_doge',
            'whatever@edracers.com',
            'pass'
        )

        # We need to ensure the `slug` & `content_html` get autopopulated here.
        post = NewsPost.objects.create(
            author=admin_user,
            title='FIRST POST~!',
            content="We maded you _an_ website, but we ated it."
        )
        self.assertEqual(post.slug, 'first-post')
        self.assertEqual(
            post.content_html, 
            '<p>We maded you <em>an</em> website, but we ated it.</p>'
        )
