from django.contrib.auth.models import User
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


class CourseTestCase(TestCase):
    def setUp(self):
        super(CourseTestCase, self).setUp()

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
            title='Shinrarta Special',
            system='Shinrarta Dezhra',
            course_type='surface',
            nearby_outfitting='Jameson Memorial, Shinrarta Dezhra',
            distance_from_primary='50.2',
            distance_from_sol='46.8',
            notes='Such canyon. Much race. Waow.',
            created_by=self.cmdr,
            is_approved=True,
            approved_by=self.admin_user
        )

    def test_approved(self):
        # We need to make sure the custom manager works correctly when
        # user-created courses are present.
        unapproved_course = Course.objects.create(
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
        self.assertEqual(Course.approved.count(), 1)
        self.assertTrue(unapproved_course not in Course.approved.all())

        # Make sure it still turns up in `Course.objects.all()` tho.
        self.assertEqual(Course.approved.count(), 1)
        self.assertTrue(unapproved_course not in Course.approved.all())

    def test_zg_vehicle_type(self):
        zg = ZeroGravityCourse.objects.create(
            course=self.course_1,
            station_name='Abraham Lincoln',
            number_of_rings=1,
            length=10
        )
        self.assertEqual(zg.vehicle_type, 'ship')

    def test_surface_vehicle_type(self):
        surface = SurfaceCourse.objects.create(
            course=self.course_1,
            planet_name='Mercury',
            coordinates='10, -25.67890',
            gravity='0.4'
        )
        self.assertEqual(surface.vehicle_type, 'ship')

    def test_rally_vehicle_type(self):
        rally = SRVRallyCourse.objects.create(
            course=self.course_1,
            planet_name='Mercury',
            start_port_name='Ehrlich City',
            end_port_name='LOLOLOLOL',
            gravity='0.4',
            length=45,
            planet_type='rock'
        )
        self.assertEqual(rally.vehicle_type, 'srv')

    def test_cross_vehicle_type(self):
        cross = SRVCrossCourse.objects.create(
            course=self.course_1,
            planet_name='Mercury',
            port_name='Ehrlich City',
            gravity='0.4',
            tidally_locked=False
        )
        self.assertEqual(cross.vehicle_type, 'srv')

    def test_stadium_vehicle_type(self):
        stadium = StadiumCourse.objects.create(
            course=self.course_1,
            planet_name='Mercury',
            port_name='Ehrlich City',
            gravity='0.4'
        )
        self.assertEqual(stadium.vehicle_type, 'ship')
