from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

import json, urllib3
from time import sleep

from models import *

@staff_member_required
def locate(request):
    c = {
       'ACTIVITY_LOGGER_GOOGLE_API_KEY':settings.ACTIVITY_LOGGER_GOOGLE_API_KEY, 
    }
    return render(request,'activity_logger/locate.html',c)

@staff_member_required
def get_locations(request):
    entries = Entry.objects.all()
    http = urllib3.PoolManager()
    for entry in entries:
            entry.getLocation()
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    json_serializer.serialize(Location.objects.all())
    data = json_serializer.getvalue()
    return HttpResponse(data,content_type="application/json")
