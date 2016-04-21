from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.dashboard,name='activity_logger/dashboard'),
    url(r'^locate/$', views.locate,name='activity_logger/locate'),
    url(r'^locate_iframe/$', views.locate_iframe,name='activity_logger/locate_iframe'),
    url(r'^get_locations/$', views.get_locations,name='activity_logger/get_locations'),
]
