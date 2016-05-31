from django.shortcuts import get_object_or_404, render

from courses.models import Course

from .models import Commander


def cmdr_detail(request, cmdr_name):
    cmdr = get_object_or_404(Commander, name=cmdr_name)
    # FIXME: Add the public-ness check here.
    courses = cmdr.course_set.all()
    return render(request, 'cmdrs/detail.html', {
        'cmdr': cmdr,
        'courses': courses,
    })
