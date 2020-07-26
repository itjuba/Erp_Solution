from django.template import Library
register = Library()


@register.filter(name='split')
def split(value, key):
    return value.split(key)