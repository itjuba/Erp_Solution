from django.template import Library

register = Library()


@register.filter
def achat(obj):
    return obj.__str__()