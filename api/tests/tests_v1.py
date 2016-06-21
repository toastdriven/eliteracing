import datetime
import json
import pytz
import urllib

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from cmdrs.models import Commander

from courses.models import (
    Course,
    ZeroGravityCourse,
    SurfaceCourse,
    SRVRallyCourse,
    SRVCrossCourse,
    StadiumCourse,
)


class APIv1CoursesTestCase(TestCase):
    def setUp(self):
        super(APIv1CoursesTestCase, self).setUp()

        self.admin_user = User.objects.create_user(
            'admin_doge',
            'whatever@edracers.com',
            'pass'
        )
        self.cmdr = Commander.objects.create(
            user=self.admin_user,
            name='Branch'
        )
        self.cmdr_2 = Commander.objects.create(
            name='FatHaggard'
        )
        self.cmdr_3 = Commander.objects.create(
            name='Coconut_Head_'
        )

        self.course_1 = Course.objects.create(
            title='Sol Classic',
            system='Sol',
            course_type='zerogravity',
            nearby_outfitting='',
            distance_from_primary='50.2',
            distance_from_sol='0.0',
            notes='The original & oft-imitated.',
            created_by=self.cmdr_3,
            created=datetime.datetime(2016, 4, 29, 9, 30, tzinfo=pytz.utc),
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
            created_by=self.cmdr_2,
            created=datetime.datetime(2016, 4, 29, 9, 31, tzinfo=pytz.utc),
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
            created_by=self.cmdr_3,
            created=datetime.datetime(2016, 4, 29, 9, 32, tzinfo=pytz.utc),
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
            created=datetime.datetime(2016, 4, 29, 9, 33, tzinfo=pytz.utc),
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
            created_by=self.cmdr_2,
            created=datetime.datetime(2016, 4, 29, 9, 34, tzinfo=pytz.utc),
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
            created=datetime.datetime(2016, 4, 29, 9, 35, 26, 167, tzinfo=pytz.utc),
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
            created=datetime.datetime(2016, 4, 29, 9, 45, tzinfo=pytz.utc),
            is_approved=False,
            approved_by=None
        )

    def make_list_url(self, **kwargs):
        list_url = reverse('api_course_list')

        if kwargs:
            list_url += '?' + urllib.urlencode(kwargs)

        return list_url

    def make_detail_url(self, course):
        return reverse(
            'api_course_detail',
            kwargs={
                'pk': course.pk,
            }
        )

    def assertCourses(self, data, expected_courses):
        return self.assertEqual(
            [course['id'] for course in data['courses']],
            [course.pk for course in expected_courses],
        )

    def test_list(self):
        resp = self.client.get(self.make_list_url())
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data['meta'], {
            'limit': 100,
            'start': None,
            'total': 6,
        })

        # Ensure the unapproved doesn't show up here.
        self.assertEqual(len(data['courses']), 6)

        # Descending order by created by default.
        self.assertEqual(data['courses'][0]['title'], self.course_6.title)

    def test_list_invalid_start(self):
        resp = self.client.get(self.make_list_url(
            start='abc'
        ))
        self.assertEqual(resp.status_code, 400)

    def test_list_invalid_order(self):
        resp = self.client.get(self.make_list_url(
            order='Small veggie burger w/ sweet potato fries, hold the pickles'
        ))
        self.assertEqual(resp.status_code, 400)

    def test_list_invalid_limit(self):
        resp = self.client.get(self.make_list_url(
            limit='1001'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data['meta']['limit'], 1000)

    def test_list_ordering(self):
        resp = self.client.get(self.make_list_url(
            order='asc'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data['meta'], {
            'limit': 100,
            'start': None,
            'total': 6,
        })

        # Ensure the unapproved doesn't show up here.
        self.assertEqual(len(data['courses']), 6)

        # Should be ascending order.
        self.assertEqual(data['courses'][0]['title'], self.course_1.title)

    def test_list_start(self):
        resp = self.client.get(self.make_list_url(
            start=self.course_3.pk
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data['meta'], {
            'limit': 100,
            'start': self.course_3.pk,
            # Total is still 6, because that's the whole set.
            'total': 6,
        })
        # But there should be only 4 results, due to the `start`.
        self.assertCourses(data, [
            self.course_6,
            self.course_5,
            self.course_4,
            self.course_3,
        ])

    def test_list_start_and_order(self):
        resp = self.client.get(self.make_list_url(
            start=self.course_3.pk,
            order='asc',
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data['meta'], {
            'limit': 100,
            'start': self.course_3.pk,
            # Total is still 6, because that's the whole set.
            'total': 6,
        })
        # But there should be only 4 results, due to the `start`.
        self.assertCourses(data, [
            self.course_3,
            self.course_4,
            self.course_5,
            self.course_6,
        ])

    def test_list_start_and_order_and_limit(self):
        resp = self.client.get(self.make_list_url(
            start=self.course_2.pk,
            order='asc',
            limit=2
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data['meta'], {
            'limit': 2,
            'start': self.course_2.pk,
            # Total is still 6, because that's the whole set.
            'total': 6,
        })
        # But there should be only 2 results, due to the `start` & `limit`.
        self.assertCourses(data, [
            self.course_2,
            self.course_3,
        ])

    def test_list_vehicle_type_all(self):
        resp = self.client.get(self.make_list_url(
            vehicle_type='all'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_6,
            self.course_5,
            self.course_4,
            self.course_3,
            self.course_2,
            self.course_1,
        ])

    def test_list_vehicle_type_ship(self):
        resp = self.client.get(self.make_list_url(
            vehicle_type='ship'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_6,
            self.course_3,
            self.course_2,
            self.course_1,
        ])

    def test_list_vehicle_type_srv(self):
        resp = self.client.get(self.make_list_url(
            vehicle_type='srv'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_5,
            self.course_4,
        ])

    def test_list_course_type_all(self):
        resp = self.client.get(self.make_list_url(
            course_type='all'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_6,
            self.course_5,
            self.course_4,
            self.course_3,
            self.course_2,
            self.course_1,
        ])

    def test_list_course_type_zerogravity(self):
        resp = self.client.get(self.make_list_url(
            course_type='zerogravity'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_2,
            self.course_1,
        ])

    def test_list_course_type_rally(self):
        resp = self.client.get(self.make_list_url(
            course_type='srvrally'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_4,
        ])

    def test_list_system_sol(self):
        resp = self.client.get(self.make_list_url(
            system='sol'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_6,
            self.course_5,
            self.course_4,
            self.course_3,
            self.course_2,
            self.course_1,
        ])

    def test_list_system_shinrarta(self):
        resp = self.client.get(self.make_list_url(
            system='SHINRARTA DEZHRA'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [])

    def test_list_cmdr_branch(self):
        resp = self.client.get(self.make_list_url(
            created_by='branch'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_6,
            self.course_4,
        ])

    def test_list_cmdr_fathaggard(self):
        resp = self.client.get(self.make_list_url(
            created_by='FatHaggard'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_5,
            self.course_2,
        ])

    def test_list_cmdr_coconut_head_(self):
        resp = self.client.get(self.make_list_url(
            created_by='Coconut_head_'
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertCourses(data, [
            self.course_3,
            self.course_1,
        ])

    def test_detail_zerogravity(self):
        resp = self.client.get(self.make_detail_url(
            self.course_1
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data, {
            'course_info': {
                'length': 10,
                'number_of_rings': 1,
                'station_name': u'Abraham Lincoln',
                'vehicle_type': u'ship'
            },
            'course_type': u'zerogravity',
            'created': 1461922200000,
            'created_by': u'Coconut_Head_',
            'distance_from_primary': u'50.20',
            'distance_from_sol': u'0.00',
            'id': self.course_1.pk,
            'nearby_outfitting': u'',
            'notes': u'The original & oft-imitated.',
            'screenshots': [],
            'system': u'Sol',
            'title': u'Sol Classic',
            'url': u'/courses/{}/'.format(self.course_1.pk)
        })

    def test_detail_surface(self):
        resp = self.client.get(self.make_detail_url(
            self.course_3
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data, {
            'course_info': {
                'coordinates': u'10, -25.67890',
                'gravity': u'0.40',
                'planet_name': u'Mercury',
                'vehicle_type': u'ship'
            },
            'course_type': u'surface',
            'created': 1461922320000,
            'created_by': u'Coconut_Head_',
            'distance_from_primary': u'50.20',
            'distance_from_sol': u'0.00',
            'id': self.course_3.pk,
            'nearby_outfitting': u'',
            'notes': u'Such canyon. Much race. Waow.',
            'screenshots': [],
            'system': u'Sol',
            'title': u'Sol Survivor',
            'url': u'/courses/{}/'.format(self.course_3.pk)
        })

    def test_detail_srvrally(self):
        resp = self.client.get(self.make_detail_url(
            self.course_4
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data, {
            'course_info': {
                'end_port_name': u'LOLOLOLOL',
                'finish_line': u'',
                'gravity': u'0.40',
                'length': 45,
                'planet_name': u'Mercury',
                'planet_type': u'rock',
                'start_port_name': u'Ehrlich City',
                'starting_line': u'',
                'vehicle_type': u'srv'
            },
            'course_type': u'srvrally',
            'created': 1461922380000,
            'created_by': u'Branch',
            'distance_from_primary': u'50.20',
            'distance_from_sol': u'0.00',
            'id': self.course_4.pk,
            'nearby_outfitting': u'',
            'notes': u'Back in my day, we drove between ports! Uphill! Both ways! IN THE SNOW!',
            'screenshots': [],
            'system': u'Sol',
            'title': u'Sol-y Moley!',
            'url': u'/courses/{}/'.format(self.course_4.pk)
        })

    def test_detail_srvcross(self):
        resp = self.client.get(self.make_detail_url(
            self.course_5
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertEqual(data, {
            'course_info': {
                'gravity': u'0.40',
                'planet_name': u'Mercury',
                'port_name': u'Ehrlich City',
                'tidally_locked': False,
                'vehicle_type': u'srv'
            },
            'course_type': u'srvcross',
            'created': 1461922440000,
            'created_by': u'FatHaggard',
            'distance_from_primary': u'50.20',
            'distance_from_sol': u'0.00',
            'id': self.course_5.pk,
            'nearby_outfitting': u'',
            'notes': u'Gotta Go Fast.',
            'screenshots': [],
            'system': u'Sol',
            'title': u'2Fast2Sol',
            'url': u'/courses/{}/'.format(self.course_5.pk)
        })

    def test_detail_stadium(self):
        resp = self.client.get(self.make_detail_url(
            self.course_6
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.maxDiff = None
        self.assertEqual(data, {
            'course_info': {
                'gravity': u'0.40',
                'planet_name': u'Mercury',
                'port_name': u'Ehrlich City',
                'vehicle_type': u'ship'
            },
            'course_type': u'stadium',
            'created': 1461922526167,
            'created_by': u'Branch',
            'distance_from_primary': u'50.20',
            'distance_from_sol': u'0.00',
            'id': self.course_6.pk,
            'nearby_outfitting': u'',
            'notes': u'Death-defying loops.',
            'screenshots': [],
            'system': u'Sol',
            'title': u'Sol Special',
            'url': u'/courses/{}/'.format(self.course_6.pk)
        })

    def test_random(self):
        resp = self.client.get(reverse(
            'api_course_random_course',
        ))
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        self.assertTrue('title' in data)

