from models import *


def log_entry(request=None,content=None):
   
   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
   if x_forwarded_for:
       remote_addr = x_forwarded_for.split(',')[0]
   else:
       remote_addr = request.META.get('REMOTE_ADDR')

   e = Entry(
       http_referer = request.META.get('HTTP_REFERER'),
       http_user_agent = request.META.get('HTTP_USER_AGENT'),
       remote_addr = request.META.get('REMOTE_ADDR'),
       request_method = request.META.get('REQUEST_METHOD')[:8],
       path = request.path,
       user = request.user if not request.user.is_anonymous() else None,
       content = content,
       is_secure = request.is_secure(),
   )
   e.save()
   return e
    

