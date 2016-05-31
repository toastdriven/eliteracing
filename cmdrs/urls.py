from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<cmdr_name>[\w\d_.-]+)/$', views.cmdr_detail, name='cmdr_detail'),
]
