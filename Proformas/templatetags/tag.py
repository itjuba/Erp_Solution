from django.template import Library

register = Library()


@register.filter
def filter(obj):
    print(obj.name())
    return obj.name()