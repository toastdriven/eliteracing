# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.db import migrations, models


def create_course(Commander, Course, data):
    cmdr, _ = Commander.objects.get_or_create(
        name=data['created_by']
    )
    course, _ = Course.objects.get_or_create(
        title=data['title'],
        defaults={
            'system': data['system'],
            'course_type': data['course_type'],
            'nearby_outfitting': data['nearby_outfitting'],
            'distance_from_primary': data['distance_from_primary'],
            'distance_from_sol': data['distance_from_sol'],
            'notes': data['notes'],
            'created_by': cmdr,
        }
    )
    return course


def create_initial_courses(apps, schema_editor):
    Commander = apps.get_model("cmdrs", "Commander")
    Course = apps.get_model("courses", "Course")
    ZeroGravityCourse = apps.get_model("courses", "ZeroGravityCourse")
    SurfaceCourse = apps.get_model("courses", "SurfaceCourse")
    SRVRallyCourse = apps.get_model("courses", "SRVRallyCourse")
    SRVCrossCourse = apps.get_model("courses", "SRVCrossCourse")
    StadiumCourse = apps.get_model("courses", "StadiumCourse")

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data'
    )
    zg_file = os.path.join(data_dir, 'zero_gravity.json')
    surface_file = os.path.join(data_dir, 'surface.json')
    rally_file = os.path.join(data_dir, 'srvrally.json')
    cross_file = os.path.join(data_dir, 'srvcross.json')
    stadium_file = os.path.join(data_dir, 'stadium.json')

    with open(zg_file) as raw_zg_data:
        zg_data = json.load(raw_zg_data)

        for data in zg_data:
            course = create_course(Commander, Course, data)
            
            zg, _ = ZeroGravityCourse.objects.get_or_create(
                course=course,
                defaults={
                    "vehicle_type": data['course_info']['vehicle_type'],
                    "station_name": data['course_info']['station_name'],
                    "number_of_rings": data['course_info']['number_of_rings'],
                    "length": data['course_info']['length'],
                }
            )

    with open(surface_file) as raw_surface_data:
        surface_data = json.load(raw_surface_data)

        for data in surface_data:
            course = create_course(Commander, Course, data)

            surface, _ = SurfaceCourse.objects.get_or_create(
                course=course,
                defaults={
                    "vehicle_type": data['course_info']['vehicle_type'],
                    "planet_name": data['course_info']['planet_name'],
                    "coordinates": data['course_info']['coordinates'],
                    "gravity": data['course_info']['gravity'],
                }
            )

    with open(rally_file) as raw_rally_data:
        rally_data = json.load(raw_rally_data)

        for data in rally_data:
            course = create_course(Commander, Course, data)

            rally, _ = SRVRallyCourse.objects.get_or_create(
                course=course,
                defaults={
                    "vehicle_type": data['course_info']['vehicle_type'],
                    "planet_name": data['course_info']['planet_name'],
                    "length": data['course_info']['length'],
                    "start_port_name": data['course_info']['start_port_name'],
                    "end_port_name": data['course_info']['end_port_name'],
                    "starting_line": data['course_info']['starting_line'],
                    "finish_line": data['course_info']['finish_line'],
                    "gravity": data['course_info']['gravity'],
                    "planet_type": data['course_info']['planet_type'],
                }
            )

    with open(cross_file) as raw_cross_data:
        cross_data = json.load(raw_cross_data)

        for data in cross_data:
            course = create_course(Commander, Course, data)

            cross, _ = SRVCrossCourse.objects.get_or_create(
                course=course,
                defaults={
                    "vehicle_type": data['course_info']['vehicle_type'],
                    "planet_name": data['course_info']['planet_name'],
                    "port_name": data['course_info']['port_name'],
                    "gravity": data['course_info']['gravity'],
                    "tidally_locked": data['course_info']['tidally_locked'],
                }
            )

    with open(stadium_file) as raw_stadium_data:
        stadium_data = json.load(raw_stadium_data)

        for data in stadium_data:
            course = create_course(Commander, Course, data)

            stadium, _ = StadiumCourse.objects.get_or_create(
                course=course,
                defaults={
                    "vehicle_type": data['course_info']['vehicle_type'],
                    "planet_name": data['course_info']['planet_name'],
                    "port_name": data['course_info']['port_name'],
                    "gravity": data['course_info']['gravity'],
                }
            )


class Migration(migrations.Migration):
    dependencies = [
        ('cmdrs', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_courses),
    ]