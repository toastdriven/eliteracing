from django.conf.urls import url

from .views import show_page


urlpatterns = [
    url(r'^(?P<slug>[\w\d_.-]+)/$', show_page, name='pages_show_page'),
]
