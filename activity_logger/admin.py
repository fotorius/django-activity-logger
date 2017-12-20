from django.contrib import admin
from .models import *

from django.contrib.admin.filters import SimpleListFilter

#i18n
from django.utils.translation import ugettext_lazy as _

class UserFilterSpec(SimpleListFilter):
    title = u'User'
    parameter_name = u'user'
    
    def lookups(self, request, model_admin):
        return (
            ('0', _('Anonymous'), ),
            ('1', _('Authenticated'), ),
            ('2', _('Staff'), ),
            ('3', _('Not Staff'), ),
        )
    def queryset(self, request, queryset):
        kwargs = {
           '%s'%self.parameter_name : None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        if self.value() == '2':
            return queryset.filter(user__is_staff=True)
        if self.value() == '3':
            return queryset.exclude(user__is_staff=True)
        return queryset

class EntryAdmin(admin.ModelAdmin):
    list_display = ('created', 'remote_addr','http_referer','path','user','description',)
    search_fields = ('remote_addr','description','path','user__username',)
    list_filter = (UserFilterSpec,)


admin.site.register(Entry,EntryAdmin)
admin.site.register(Path)
admin.site.register(Location)
