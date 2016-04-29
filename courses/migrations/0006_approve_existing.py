# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.db import migrations, models


def approve_existing_courses(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    Course.objects.all().update(is_approved=True)


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0005_add_approval'),
    ]

    operations = [
        migrations.RunPython(approve_existing_courses),
    ]
