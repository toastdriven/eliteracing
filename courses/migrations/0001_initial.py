# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 00:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cmdrs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('system', models.CharField(max_length=255)),
                ('course_type', models.CharField(choices=[(b'zerogravity', b'Zero Gravity'), (b'surface', b'Surface'), (b'srvrally', b'SRV Rally'), (b'srvcross', b'SRV Cross'), (b'stadium', b'Stadium')], max_length=16)),
                ('nearby_outfitting', models.CharField(blank=True, default=b'', max_length=128)),
                ('distance_from_primary', models.DecimalField(decimal_places=2, default=b'0.0', max_digits=8)),
                ('distance_from_sol', models.DecimalField(decimal_places=2, default=b'0.0', max_digits=8)),
                ('notes', models.TextField(blank=True, default=b'')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdrs.Commander')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='CourseScreenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shot', models.ImageField(max_length=255, upload_to=b'')),
                ('is_primary', models.BooleanField(default=False, help_text=b'Is this the main/best image the user should see?')),
                ('is_annotated', models.BooleanField(default=False, help_text=b'Does this image have a course drawn on top of it?')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='courses.Course')),
            ],
            options={
                'ordering': ('created', 'is_primary'),
            },
        ),
        migrations.CreateModel(
            name='SRVCrossCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(blank=True, choices=[(b'ship', b'Ship'), (b'srv', b'SRV')], default=b'ship', max_length=8)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('planet_name', models.CharField(max_length=255)),
                ('port_name', models.CharField(max_length=255)),
                ('gravity', models.DecimalField(decimal_places=2, default=b'1.0', max_digits=5)),
                ('tidally_locked', models.BooleanField(default=False)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SRVRallyCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(blank=True, choices=[(b'ship', b'Ship'), (b'srv', b'SRV')], default=b'ship', max_length=8)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('planet_name', models.CharField(max_length=255)),
                ('length', models.PositiveIntegerField(help_text=b'In Kilometers')),
                ('start_port_name', models.CharField(max_length=255)),
                ('end_port_name', models.CharField(max_length=255)),
                ('starting_line', models.CharField(blank=True, default=b'', max_length=255)),
                ('finish_line', models.CharField(blank=True, default=b'', max_length=255)),
                ('gravity', models.DecimalField(decimal_places=2, default=b'1.0', max_digits=5)),
                ('planet_type', models.CharField(choices=[(b'rock', b'rock'), (b'ice', b'ice'), (b'lava', b'lava'), (b'metallic', b'metallic'), (b'water', b'water'), (b'earth-like', b'earth-like'), (b'ammonia', b'ammonia'), (b'gas', b'gas')], default=b'rock', max_length=32)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StadiumCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(blank=True, choices=[(b'ship', b'Ship'), (b'srv', b'SRV')], default=b'ship', max_length=8)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('planet_name', models.CharField(max_length=255)),
                ('port_name', models.CharField(max_length=255)),
                ('gravity', models.DecimalField(decimal_places=2, default=b'1.0', max_digits=5)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurfaceCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(blank=True, choices=[(b'ship', b'Ship'), (b'srv', b'SRV')], default=b'ship', max_length=8)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('planet_name', models.CharField(max_length=255)),
                ('coordinates', models.CharField(max_length=64)),
                ('gravity', models.DecimalField(decimal_places=2, default=b'1.0', max_digits=5)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ZeroGravityCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(blank=True, choices=[(b'ship', b'Ship'), (b'srv', b'SRV')], default=b'ship', max_length=8)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('station_name', models.CharField(max_length=255)),
                ('number_of_rings', models.PositiveIntegerField(default=1)),
                ('length', models.PositiveIntegerField(help_text=b'In Kilometers')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]
