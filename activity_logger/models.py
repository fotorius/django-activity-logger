from django.db import models
from django.contrib.auth import get_user_model

from django.db.models import Q
import urllib3, json

#i18n
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    country = models.CharField(_('Country'),max_length=32,blank=True)
    country_code = models.CharField(_('Country Code'),max_length=2,blank=True)
    region = models.CharField(_('Region'),max_length=32,blank=True)
    region_code = models.CharField(_('Region Code'),max_length=8,blank=True)
    city = models.CharField(_('City'),max_length=32,blank=True)
    zip_code = models.CharField(_('Zip Code'),max_length=8,blank=True)
    latitude = models.FloatField(_('Latitude'),default=0)
    longitude = models.FloatField(_('Longitude'),default=0)
    timezone = models.CharField(_('Timezone'),max_length=32,blank=True) 
    isp = models.CharField(_('ISP'),max_length=32,blank=True) 
    organization = models.CharField(_('Organiztion'),max_length=32,blank=True) 
    as_name = models.CharField(_('AS number/name'),max_length=32,blank=True) 
    created = models.DateTimeField(_('Created'),auto_now_add=True)
    
    def __str__(self):
        if self.country and self.region:
            return "%s, %s" % (self.country,self.region)
        return str(self.created)

class Path(models.Model):
    name = models.TextField(_('Name'))

    def __str__(self):
        return self.name

    def entries(self):
        return Entry.objects.filter(path__name=self.name)

class Entry(models.Model):
    http_referer = models.CharField(_('HTTP Referer'),max_length=512,null=True)
    http_user_agent = models.TextField(_('HTTP User Agent'),null=True)
    remote_addr = models.CharField(_('Remote Address'),max_length=40)
    request_method = models.CharField(_('Request Method'),max_length=8)
    path = models.ForeignKey(Path,verbose_name=_('Path'),on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),verbose_name=_('User'),null=True,blank=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(_('Created'),auto_now_add=True)
    description = models.CharField(_('Description'),max_length=128,null=True,blank=True)
    location = models.ForeignKey(Location,verbose_name=_('Location'),null=True,blank=True,on_delete=models.SET_NULL)
    remote_addr_is_private = models.NullBooleanField(null=True)
    is_secure = models.BooleanField(_('Is Secure'),default=False)

    class Meta:
        verbose_name_plural = _('entries')
        ordering = ('-created',)
   
    def __str__(self):
        return self.description

    def get_location(self,force=False):
        """
        Gets the location from ip-api.com
        """
        # Return if location is already available
        if self.location and not force:
            return self.location
        # Return None if the ip was already proven to be private
        if self.remote_addr_is_private and not force:
            return None
  
        # Check if this IP already was identified as private
        entries = Entry.objects.filter(
            remote_addr_is_private=True,
            remote_addr=self.remote_addr
        )
        # Return last instance if IP was already located
        if entries and not force:
            self.remote_addr_is_private = True
            self.save()
            return self.location
  
        # Check if this IP already was located
        entries = Entry.objects.filter(
            location__isnull=False,
            remote_addr=self.remote_addr
        ).order_by('-location__created')
        # Return last instance if IP was already located
        if entries and not force:
            self.location = entries.first().get_location()
            self.save()
            return self.location
  
        # Get location data from ip-api.com
        http = urllib3.PoolManager()
        r = http.request('GET','http://ip-api.com/json/'+self.remote_addr)
        if r.status == 200:
            data = json.loads(r.data)
            if data.get('status') == 'success':
                location = Location(
                    country=data.get('country',''),
                    country_code=data.get('countryCode',''),
                    region=data.get('regionName',''),
                    region_code=data.get('region',''),
                    city=data.get('city',''),
                    zip_code=data.get('zip',''),
                    latitude=data.get('lat',0.0),
                    longitude=data.get('lon',0.0),
                    timezone=data.get('timezone',''),
                    isp=data.get('isp',''),
                    organization=data.get('org',''),
                    as_name=data.get('as','')
                )
                location.save()
                self.location = location
                self.save()
            else:
                self.remote_addr_is_private = True
                self.save()
  
        return self.location       
     
