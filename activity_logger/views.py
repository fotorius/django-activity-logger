from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

#i18n
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

import json
from time import sleep

from models import Entry, Location
from utils import update_entry_locations

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
        {
            'title':_('Traffic'),
            'remote':reverse('activity_logger/traffic'),
            'anchor':'traffic',
        },
    ]
    c = {
        'title':title,
        'tabs':tabs,
        'ACTIVITY_LOGGER_GOOGLE_API_KEY':settings.ACTIVITY_LOGGER_GOOGLE_API_KEY, 
    }
    return render(request,'activity_logger/dashboard.html',c)

@staff_member_required
def traffic(request):
    entries = Entry.objects.all()
    update_entry_locations(entries)
    entries = Entry.objects.all()
    c = {
        'entries':entries,
    }
    return render(request,'activity_logger/traffic.html',c)

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
    update_entry_locations(Entry.objects.all())
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    json_serializer.serialize(Location.objects.all())
    data = json_serializer.getvalue()
    return HttpResponse(data,content_type="application/json")
