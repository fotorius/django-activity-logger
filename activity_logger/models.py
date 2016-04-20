from django.db import models
from django.contrib.auth.models import User

#i18n
from django.utils.translation import ugettext_lazy as _

class Entry(models.Model):
   http_referer = models.CharField(_('HTTP Referer'),max_length=128,null=True)
   http_user_agent = models.TextField(_('HTTP User Agent'),null=True)
   remote_addr = models.CharField(_('Remote Address'),max_length=40)
   request_method = models.CharField(_('Request Method'),max_length=8)
   path = models.CharField(_('Path'),max_length=256)
   user = models.ForeignKey(User,verbose_name=_('User'),null=True,blank=True)
   created = models.DateTimeField(_('Created'),auto_now_add=True)
   content = models.CharField(_('Content'),max_length=128)
   latitude = models.FloatField(_('Latitude'),default=0)
   longitude = models.FloatField(_('Longitude'),default=0)
   country = models.CharField(_('Country'),max_length=2,blank=True)

   class Meta:
       verbose_name_plural = _('entries')
   
   def __unicode__(self):
       return self.content
