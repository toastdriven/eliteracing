from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase

from cmdrs.models import Commander

from ..models import (
    Course,
    ZeroGravityCourse,
    SurfaceCourse,
    SRVRallyCourse,
    SRVCrossCourse,
    StadiumCourse,
)


class CourseViewsTestCase(TestCase):
    def setUp(self):
        super(CourseViewsTestCase, self).setUp()

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

        self.course_2 = Course.objects.create(
            title='Sol Skywalker',
            system='Sol',
            course_type='zerogravity',
            nearby_outfitting='',
            distance_from_primary='50.2',
            distance_from_sol='0.0',
            notes='Red Leader, standing by.',
            created_by=self.cmdr,
            is_approved=True,
            approved_by=self.admin_user
        )
        self.zg_2 = ZeroGravityCourse.objects.create(
            course=self.course_2,
            station_name='Daedalus',
            number_of_rings=2,
            length=17
        )

        self.course_3 = Course.objects.create(
            title='Sol Survivor',
            system='Sol',
            course_type='surface',
            nearby_outfitting='',
            distance_from_primary='50.2',
            distance_from_sol='0.0',
            notes='Such canyon. Much race. Waow.',
            created_by=self.cmdr,
            is_approved=True,
            approved_by=self.admin_user
        )
        self.surface_1 = SurfaceCourse.objects.create(
            course=self.course_3,
            planet_name='Mercury',
            coordinates='10, -25.67890',
            gravity='0.4'
        )

        self.course_4 = Course.objects.create(
            title='Sol-y Moley!',
            system='Sol',
            course_type='srvrally',
            nearby_outfitting='',
            distance_from_primary='50.2',
            distance_from_sol='0.0',
            notes='Back in my day, we drove between ports! Uphill! Both ways! IN THE SNOW!',
            created_by=self.cmdr,
            is_approved=True,
            approved_by=self.admin_user
        )
        self.rally_1 = SRVRallyCourse.objects.create(
            course=self.course_4,
            planet_name='Mercury',
            start_port_name='Ehrlich City',
            end_port_name='LOLOLOLOL',
            gravity='0.4',
            length=45,
            planet_type='rock'
        )

        self.course_5 = Course.objects.create(
            title='2Fast2Sol',
            system='Sol',
            course_type='srvcross',
            nearby_outfitting='',
            distance_from_primary='50.2',
            distance_from_sol='0.0',
            notes='Gotta Go Fast.',
            created_by=self.cmdr,
            is_approved=True,
            approved_by=self.admin_user
        )
        self.cross_1 = SRVCrossCourse.objects.create(
            course=self.course_5,
            planet_name='Mercury',
            port_name='Ehrlich City',
            gravity='0.4',
            tidally_locked=False
        )

        self.course_6 = Course.objects.create(
            title='Sol Special',
            system='Sol',
            course_type='stadium',
            nearby_outfitting='',
            distance_from_primary='50.2',
            distance_from_sol='0.0',
            notes='Death-defying loops.',
            created_by=self.cmdr,
            is_approved=True,
            approved_by=self.admin_user
        )
        self.stadium_1 = StadiumCourse.objects.create(
            course=self.course_6,
            planet_name='Mercury',
            port_name='Ehrlich City',
            gravity='0.4'
        )

        self.unapproved_course = Course.objects.create(
            title='Sol Scramble',
            system='Sol',
            course_type='zerogravity',
            nearby_outfitting='Abraham Lincoln, Sol',
            distance_from_primary='251.1',
            distance_from_sol='0.0',
            notes="Don't try this at home.",
            created_by=self.cmdr,
            is_approved=False,
            approved_by=None
        )

        self.list_url = reverse('courses_list')
        self.detail_url = reverse(
            'courses_detail', 
            kwargs={
                'id': self.course_2.pk,
            }
        )

    def test_list(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        # Ensure the unapproved doesn't show up here.
        self.assertEqual(len(resp.context['page']), 6)
        self.assertTrue(self.course_1 in resp.context['page'])
        self.assertEqual(resp.context['vehicle_type'], 'all')
        self.assertEqual(resp.context['course_type'], 'all')

    def test_list_invalid_page(self):
        resp = self.client.get(self.list_url + '?page=200')
        self.assertEqual(resp.status_code, 404)

    def test_list_filtering_vehicle_type(self):
        resp = self.client.get(self.list_url + '?vehicle_type=ship')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page']), 4)
        self.assertTrue(self.course_6 in resp.context['page'])
        self.assertEqual(resp.context['vehicle_type'], 'ship')
        self.assertEqual(resp.context['course_type'], 'all')

    def test_list_filtering_course_type(self):
        resp = self.client.get(self.list_url + '?course_type=zerogravity')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['page']), 2)
        self.assertTrue(self.course_2 in resp.context['page'])
        self.assertEqual(resp.context['vehicle_type'], 'all')
        self.assertEqual(resp.context['course_type'], 'zerogravity')

    def test_detail(self):
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['course'].title, self.course_2.title)

    def test_detail_invalid_pk(self):
        resp = self.client.get(reverse(
            'courses_detail',
            kwargs={
                'id': 100000000,
            }
        ))
        self.assertEqual(resp.status_code, 404)
