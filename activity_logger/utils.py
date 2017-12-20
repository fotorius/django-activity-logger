from .models import Entry, Location, Path


def update_entry_locations(queryset):
    """
    Update the locations of certian queryset of Entries
    """
    for entry in queryset:
            entry.get_location()


def log_entry(request,description=None):
    """
    This method will log an entry made by the user, pulling its data from
    Django's request object.
    A description string may be added to further the information about this
    request.
    """   
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        remote_addr = x_forwarded_for.split(',')[0]
    else:
        remote_addr = request.META.get('REMOTE_ADDR')
    
    try:
        path = Path.objects.get(name=request.path)
    except Path.MultipleObjectsReturned:
        paths = Path.objects.filter(name=request.path)
        path = paths[0]
    except Path.DoesNotExist:
        path = Path(name=request.path)
        path.save()
 
    
    e = Entry(
        http_referer = request.META.get('HTTP_REFERER'),
        http_user_agent = request.META.get('HTTP_USER_AGENT'),
        remote_addr = request.META.get('REMOTE_ADDR'),
        path=path,
        request_method = request.META.get('REQUEST_METHOD')[:8],
        user = request.user if not request.user.is_anonymous else None,
        description = description,
        is_secure = request.is_secure(),
    )
    e.save()
    return e
       
