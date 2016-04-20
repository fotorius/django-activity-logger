
from ..models import *
from ..utils import *


class ActivityLoggerMiddleware(object):
    # Log Activity
    def process_request(self, request):
       request.log_entry = log_entry(request,'')
       return None
