from django import template
from django.template.defaultfilters import length

register = template.Library()

@register.filter(name='length_is')
def length_is(value, arg):
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False