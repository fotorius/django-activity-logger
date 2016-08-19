
from activity_logger.utils import log_entry


class ActivityLoggerMiddleware(object):
    # Log Activity
    def process_request(self, request):
       request.log_entry = log_entry(request,'')
       return None
