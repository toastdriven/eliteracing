from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Course


def list(request):
    qs = Course.approved.all()
    course_types = [ct[0] for ct in Course.COURSE_TYPES]

    search = request.GET.get('q', None)
    vehicle_type = request.GET.get('vehicle_type', 'all')
    course_type = request.GET.get('course_type', 'all')

    if search:
        qs = qs.filter(
            Q(title__icontains=search) |
            Q(system__icontains=search) |
            Q(notes__icontains=search) |
            Q(created_by__name__icontains=search)
        )

    if vehicle_type == 'ship':
        qs = qs.filter(
            Q(course_type='zerogravity') |
            Q(course_type='surface') |
            Q(course_type='stadium')
        )
    elif vehicle_type == 'srv':
        qs = qs.filter(
            Q(course_type='srvrally') |
            Q(course_type='srvcross')
        )

    if course_type in course_types:
        qs = qs.filter(course_type=course_type)

    paginator = Paginator(qs, 20)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except (EmptyPage, ValueError):
        raise Http404("No such page.")

    return render(request, 'courses/list.html', {
        'page': page,
        'vehicle_type': vehicle_type,
        'course_type': course_type,
    })


def detail(request, id):
    course = get_object_or_404(Course.approved.all(), pk=id)
    return render(request, 'courses/detail.html', {
        'course': course,
    })
