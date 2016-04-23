from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from datetime import timedelta

#i18n
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

import json
from time import sleep

from models import Entry, Location
from utils import update_entry_locations
from forms import SearchEntriesForm 

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
    """
    Returns the list of entries on an specific list of filters.
    """
    # Update all Entries
    filtered_entries = Entry.objects.all()

    # If there is an implemented filter
    if request.method == 'POST':
       form = SearchEntriesForm(request.POST)
       if form.is_valid():
           # Filter Dates
           filtered_entries = filtered_entries.filter(created__gte=form.cleaned_data['start_date'])
           filtered_entries = filtered_entries.filter(created__lte=form.cleaned_data['end_date']+timedelta(days=2))


           # Filter Users
           if form.cleaned_data['users'] == form.ANONYMOUS:
               filtered_entries = filtered_entries.filter(user__isnull=True)
           elif form.cleaned_data['users'] == form.AUTHENTICATED:
               filtered_entries = filtered_entries.filter(user__isnull=False)
           elif form.cleaned_data['users'] == form.NOT_STAFF:
               filtered_entries = filtered_entries.filter(user__isnull=False,user__is_staff=False)
           elif form.cleaned_data['users'] == form.STAFF:
               filtered_entries = filtered_entries.filter(user__is_staff=True)
            
           # Display By
           display_by = form.cleaned_data['display_by']

           # Graph type
           graph = form.cleaned_data['graph']

    else:
        # Initialize form
        form = SearchEntriesForm(initial={
            'start_date':filtered_entries.last().created-timedelta(days=1),
            'end_date':filtered_entries.first().created,
        })
        display_by = form.fields['display_by'].initial
        graph = form.fields['graph'].initial
    
    """
    TODO: Show more information about the traffic such as location count and 
    most visited pages
    """
    update_entry_locations(filtered_entries)
    
    # Calculate graph
    entries = []
    max = 0

    if display_by == form.DAY_OF_THE_MONTH:
        for i in range(1,32):
            entries.append(filtered_entries.filter(created__day=i))
            if entries[i-1].count() > max:
                max = entries[i-1].count()
    
    elif display_by == form.DAY_OF_THE_WEEK:
        for i in range(1,8):
            entries.append(filtered_entries.filter(created__week_day=i))
            if entries[i-1].count() > max:
                max = entries[i-1].count()
    
    elif display_by == form.TIME_OF_THE_DAY:
        for i in range(0,24):
            entries.append(filtered_entries.filter(created__hour=i))
            if entries[i].count() > max:
                max = entries[i].count()
    
    elif display_by == form.YEAR:
        i = 0
        for year in range(filtered_entries.first().created.year,filtered_entries.last().created.year+1):
            entries.append(filtered_entries.filter(created__year=year))
            if entries[i].count() > max:
                max = entries[i].count()
            i += 1
    
    c = {
        'entries':entries,
        'max':max,
        'graph_height':300,
        'graph_width':950,
        'form':form,
        'action':reverse('activity_logger/traffic'),
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
