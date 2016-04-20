from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^locate/$', views.locate,name='activity_logger/locate'),
    url(r'^get_locations/$', views.get_locations,name='activity_logger/get_locations'),
]
