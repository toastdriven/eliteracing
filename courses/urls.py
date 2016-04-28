from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.list, name='courses_list'),
    url(r'^(?P<id>\d+)/$', views.detail, name='courses_detail'),
]
