from django.conf.urls import re_path, include
from . import views

urlpatterns = [
    # Dashboard
    re_path(r'^$', views.dashboard,name='activity_logger/dashboard'),
    
    # Dashboard: Locations
    re_path(r'^locate/$', views.locate,name='activity_logger/locate'),
    re_path(r'^locate_iframe/$', views.locate_iframe,name='activity_logger/locate_iframe'),
    re_path(r'^get_locations/$', views.get_locations,name='activity_logger/get_locations'),
    # Dashboard: Traffic
    re_path(r'^traffic/$', views.traffic,name='activity_logger/traffic'),

    # Dashboard: Path
    re_path(r'^path/(?P<id>\d+)/$', views.path,name='activity_logger/path'),

    # Dashboard: Entry
    re_path(r'^entry/(?P<id>\d+)/$', views.entry,name='activity_logger/entry'),

]
