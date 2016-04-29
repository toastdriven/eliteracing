import datetime
import pytz

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import NewsPost


class NewsPostViewTestCase(TestCase):
    def setUp(self):
        super(NewsPostViewTestCase, self).setUp()
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

    def test_latest(self):
        resp = self.client.get(reverse('news_latest'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            [post.title for post in resp.context['page']], 
            [self.post_2.title, self.post_1.title]
        )

    def test_year(self):
        resp = self.client.get(reverse(
            'news_by_year',
            kwargs={
                'year': '2016',
            }
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['posts']), 2)
        # Descending order!
        self.assertEqual(resp.context['posts'][0].title, self.post_2.title)

    def test_month(self):
        resp = self.client.get(reverse(
            'news_by_month',
            kwargs={
                'year': '2016',
                'month': '04',
            }
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['posts']), 2)
        # Descending order!
        self.assertEqual(resp.context['posts'][0].title, self.post_2.title)

    def test_day(self):
        resp = self.client.get(reverse(
            'news_by_day',
            kwargs={
                'year': '2016',
                'month': '04',
                'day': '23',
            }
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['posts']), 1)
        self.assertEqual(resp.context['posts'][0].title, self.post_1.title)

    def test_detail(self):
        resp = self.client.get(reverse(
            'news_post_detail',
            kwargs={
                'year': '2016',
                'month': '04',
                'day': '29',
                'slug': self.post_2.slug
            }
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['post'].title, self.post_2.title)

    def test_detail_404(self):
        resp = self.client.get(reverse(
            'news_post_detail',
            kwargs={
                'year': '2016',
                'month': '05',
                'day': '01',
                'slug': self.post_2.slug
            }
        ))
        self.assertEqual(resp.status_code, 404)
