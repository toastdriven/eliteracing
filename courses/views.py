from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Course


def list(request):
    paginator = Paginator(Course.objects.all(), 20)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except (EmptyPage, ValueError):
        raise Http404("No such page.")

    return render(request, 'courses/list.html', {
        'page': page,
    })


def detail(request, id):
    course = get_object_or_404(Course, pk=id)
    return render(request, 'courses/detail.html', {
        'course': course,
    })
