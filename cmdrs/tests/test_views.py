from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from courses.models import Course, ZeroGravityCourse

from ..models import Commander


class TestCmdrViews(TestCase):
    def setUp(self):
        super(TestCmdrViews, self).setUp()
        self.admin_user = User.objects.create_user(
            'admin_doge',
            'whatever@edracers.com',
            'pass'
        )
        self.cmdr = Commander.objects.create(
            user=self.admin_user,
            name='Branch'
        )

        self.course_1 = Course.objects.create(
            title='Sol Classic',
            system='Sol',
            course_type='zerogravity',
            nearby_outfitting='',
            distance_from_primary='50.2',
            distance_from_sol='0.0',
            notes='The original & oft-imitated.',
            created_by=self.cmdr,
            is_approved=True,
            approved_by=self.admin_user
        )
        self.zg_1 = ZeroGravityCourse.objects.create(
            course=self.course_1,
            station_name='Abraham Lincoln',
            number_of_rings=1,
            length=10
        )

    def test_detail(self):
        url = reverse('cmdr_detail', kwargs={'cmdr_name': 'Branch'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['cmdr'].pk, self.cmdr.pk)
        self.assertEqual(len(resp.context['courses']), 1)

    def test_detail_not_found(self):
        url = reverse('cmdr_detail', kwargs={'cmdr_name': 'Braben'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
