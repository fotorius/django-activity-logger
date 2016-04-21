# Django Activity Logger

This is a relatively simple middleware written for Django that
takes advantage of its request.META object. It can be implemented
with other modules and can be accessed through views to allow
field modification.

## Installation

Install in your environment:
```
pip install git+https://github.com/devalfrz/django-activity-logger
```

Incude the app in the `INSTALLED_APPS` section of your project:
```
INSTALLED_APPS = (
    ...
    'activity_logger',
    ...
)
```
Also add the corresponding middleware class: 
```
MIDDLEWARE_CLASSES = [
    ...
    'activity_logger.middleware.activity_logger.ActivityLoggerMiddleware',
    ...
]
```
Finally migrate
```
$ migrate
```

## Usage

Django Activity Logger will track all activity and will be shown in the
admin site. There are several filters that can be used to aquire your
specific need.

### Getting Locations

Using this tool you can retreive the location of your requests using
http://ip-api.com. Simply add the url to your urls.py file.
```
urlpatterns = [
   ...    
    url(r'^activity_logger/', include('activity_logger.urls')),
   ...
```
And add your Google API Key (https://console.developers.google.com/)
to your settings file.
```
ACTIVITY_LOGGER_GOOGLE_API_KEY = 'your-api-key'
```
You can have access to the dashboard by going to:
```
http://your-awesome-project.com/activity_logger
```
