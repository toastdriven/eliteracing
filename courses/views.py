from django.http import Http404
from django.shortcuts import get_object_or_404, render


def list(request):
    return render(request, 'courses/list.html', {})


def detail(request, pk):
    course = get_object_or_404(Course, pk=id)
    return render(request, 'courses/detail.html', {
        'course': course,
    })
