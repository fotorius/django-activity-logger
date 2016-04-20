from models import *


def log_entry(request=None,content=None):
   
   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
   if x_forwarded_for:
       remote_addr = x_forwarded_for.split(',')[0]
   else:
       remote_addr = request.META.get('REMOTE_ADDR')[:40]

   http_referer = request.META.get('HTTP_REFERER')
   http_user_agent = request.META.get('HTTP_USER_AGENT') 
   e = Entry(
       http_referer = None if not http_referer else http_referer[:128],
       http_user_agent = None if not http_user_agent else http_user_agent[:128],
       remote_addr = request.META.get('REMOTE_ADDR')[:40],
       request_method = request.META.get('REQUEST_METHOD')[:8],
       path = request.path[:256],
       user = request.user if not request.user.is_anonymous() else None,
       content = content[:128],
   )
   e.save()
   return e
    

