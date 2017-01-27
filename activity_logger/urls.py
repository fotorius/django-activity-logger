from django.conf.urls import url, include
import views

urlpatterns = [
    # Dashboard
    url(r'^$', views.dashboard,name='activity_logger/dashboard'),
    
    # Dashboard: Locations
    url(r'^locate/$', views.locate,name='activity_logger/locate'),
    url(r'^locate_iframe/$', views.locate_iframe,name='activity_logger/locate_iframe'),
    url(r'^get_locations/$', views.get_locations,name='activity_logger/get_locations'),
    # Dashboard: Traffic
    url(r'^traffic/$', views.traffic,name='activity_logger/traffic'),

    # Dashboard: Path
    url(r'^path/(?P<id>\d+)/$', views.path,name='activity_logger/path'),

    # Dashboard: Entry
    url(r'^entry/(?P<id>\d+)/$', views.entry,name='activity_logger/entry'),

]
