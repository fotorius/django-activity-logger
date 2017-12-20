from ..utils import log_entry

def ActivityLoggerMiddleware(get_response):
    # Log Activity
    def process_request(request):
       request.log_entry = log_entry(request,'')
       return get_response(request)

    return process_request
