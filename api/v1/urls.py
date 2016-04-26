from django.conf.urls import url, include

from .resources import (
    CourseResource,
)


urlpatterns = [
    url(r'^courses/', include(CourseResource.urls())),
]
