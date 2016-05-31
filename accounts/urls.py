from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/$', views.login_view, name='accounts_login'),
    url(r'^logout/$', views.logout_view, name='accounts_logout'),
    url(r'^register/$', views.register, name='accounts_register'),
]
