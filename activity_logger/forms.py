from django import forms

#i18n
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

class SearchEntriesForm(forms.Form):
    ALL = '0'
    ANONYMOUS = '1'
    AUTHENTICATED = '2'
    NOT_STAFF = '3'
    STAFF = '4'

    USER_CHOICES = (
        (ALL,_('All')),
        (ANONYMOUS,_('Anonymous')),
        (AUTHENTICATED,_('Authenticated')),
        (NOT_STAFF,_('Not Staff')),
        (STAFF,_('Staff')),
    )

    DAY_OF_THE_MONTH = '0'
    DAY_OF_THE_WEEK = '1'
    TIME_OF_THE_DAY = '2'
    MONTH = '3'
    YEAR = '4'

    DISPLAY_BY_CHOICES = (
        (DAY_OF_THE_MONTH,_('Day of the Month')),
        (DAY_OF_THE_WEEK,_('Day of the Week')),
        (TIME_OF_THE_DAY,_('Time of the day')),
        (MONTH,_('Month')),
        (YEAR,_('Year')),
    )
    
    start_date = forms.DateField(label=_('Start Date'),
        widget=forms.DateInput(attrs={'type':'date'})
    )
    end_date = forms.DateField(label=_('End Date'),
        widget=forms.DateInput(attrs={'type':'date'})
    )
    users = forms.ChoiceField(label=_('Users'),initial=ALL,choices=USER_CHOICES)
    display_by = forms.ChoiceField(label=_('Display By'),initial=DAY_OF_THE_MONTH,choices=DISPLAY_BY_CHOICES)
    path = forms.CharField(label=_('Path'),required=False, widget=forms.TextInput(attrs={'placeholder': _('All')}))
