from django.conf.urls import url

from .views import (
    latest_posts, 
    posts_by_year, 
    posts_by_month, 
    posts_by_day, 
    post_detail,
)


urlpatterns = [
    url(
        r'^$', 
        latest_posts, 
        name='news_latest'
    ),
    url(
        r'^(?P<year>\d{4})/$', 
        posts_by_year, 
        name='news_by_year'
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 
        posts_by_month, 
        name='news_by_month'
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', \
        posts_by_day, 
        name='news_by_day'
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w\d_.-]+)/$', 
        post_detail, 
        name='news_post_detail'
    ),
]
