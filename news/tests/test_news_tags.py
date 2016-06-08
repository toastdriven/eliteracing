import datetime
import pytz

from django.contrib.auth.models import User
from django.test import TestCase

from ..models import NewsPost
from ..templatetags.news_tags import get_latest_posts


class TestNewsTemplateTags(TestCase):
    def setUp(self):
        super(TestNewsTemplateTags, self).setUp()
        self.admin_user = User.objects.create_user(
            'admin_doge',
            'whatever@edracers.com',
            'pass'
        )

        self.post_1 = NewsPost.objects.create(
            author=self.admin_user,
            title='FIRST POST~!',
            content="We maded you _an_ website, but we ated it.",
            created=datetime.datetime(2016, 4, 23, tzinfo=pytz.utc)
        )
        self.post_2 = NewsPost.objects.create(
            author=self.admin_user,
            title='New Feature OMG',
            content="You cans naow submit coursez here.",
            created=datetime.datetime(2016, 4, 29, tzinfo=pytz.utc)
        )

    def test_get_latest_posts(self):
        posts = get_latest_posts()
        self.assertEqual(len(posts), 2)
        # Should be in descending order.
        self.assertEqual(posts[0].title, self.post_2.title)
        self.assertEqual(posts[1].title, self.post_1.title)

    def test_get_latest_posts_limit(self):
        posts = get_latest_posts(limit=1)
        self.assertEqual(len(posts), 1)
        # Should be in descending order.
        self.assertEqual(posts[0].title, self.post_2.title)
