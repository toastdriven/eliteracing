from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import NewsPost


def latest_posts(request):
    paginator = Paginator(NewsPost.objects.all(), 5)
    
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except (ValueError, EmptyPage):
        return Http404("No such page")

    return render(request, 'news/latest.html', {
        'page': page,
    })


def posts_by_year(request, year):
    posts = NewsPost.objects.filter(
        created__year=int(year)
    )
    return render(request, 'news/posts_by_year.html', {
        'posts': posts,
    })


def posts_by_month(request, year, month, day):
    posts = NewsPost.objects.filter(
        created__year=int(year),
        created__month=int(month)
    )
    return render(request, 'news/posts_by_month.html', {
        'posts': posts,
    })


def posts_by_day(request, year, month, day):
    posts = NewsPost.objects.filter(
        created__year=int(year),
        created__month=int(month),
        created__day=int(day),
    )
    return render(request, 'news/posts_by_day.html', {
        'posts': posts,
    })


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        created__year=int(year),
        created__month=int(month),
        created__day=int(day),
        slug=slug
    )
    return render(request, 'news/post_detail.html', {
        'post': post,
    })
