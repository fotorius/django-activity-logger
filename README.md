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
