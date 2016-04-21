from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

#i18n
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

import json, urllib3
from time import sleep

from models import *

@staff_member_required
def dashboard(request):
    """
    This view will show the dashboard of the activity logger.
    """
    title = _('Dashboard')
    tabs = [
        {
            'title':_('Locations'),
            'remote':reverse('activity_logger/locate'),
            'anchor':'locations',
        },
    ]
    c = {
        'title':title,
        'tabs':tabs,
        'ACTIVITY_LOGGER_GOOGLE_API_KEY':settings.ACTIVITY_LOGGER_GOOGLE_API_KEY, 
    }
    return render(request,'activity_logger/dashboard.html',c)

@staff_member_required
def locate_iframe(request):
    """
    Shows a simple page with the map to be shown inside an iframe.
    """
    c = {
        'ACTIVITY_LOGGER_GOOGLE_API_KEY':settings.ACTIVITY_LOGGER_GOOGLE_API_KEY, 
    }
    return render(request,'activity_logger/locate-iframe.html',c)

@staff_member_required
def locate(request):
    """
    Shows the map of the locations obtained by the activity logger. This
    page calls get_locations using AJAX which is who makes the heavy
    lifting.
    """
    return render(request,'activity_logger/locate.html',{})

@staff_member_required
def get_locations(request):
    """
    Returns a JSON string with the processed locations for all the entries
    available in the database.
    Calling this function will update the entries with its corresponding
    location.
    """
    entries = Entry.objects.all()
    http = urllib3.PoolManager()
    for entry in entries:
            entry.get_location()
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    json_serializer.serialize(Location.objects.all())
    data = json_serializer.getvalue()
    return HttpResponse(data,content_type="application/json")
