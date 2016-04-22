from django import template
register = template.Library()

@register.filter
def divide( value, arg ):
    try:
        return value/float(arg)
    except:
        return None

@register.filter
def multiply( value, arg ):
    return value*arg;
