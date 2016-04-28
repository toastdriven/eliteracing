from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.list, name='docs_list'),
    url(
        r'^api/v1/courses/$', 
        views.detail, 
        {
            'title': 'API v1 - Courses',
            'source': 'api/v1/courses.md',
        },
        name='docs_api_v1_courses'
    ),
]
