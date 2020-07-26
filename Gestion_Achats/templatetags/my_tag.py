from django.template import Library

register = Library()


@register.filter
def achat(obj):
    print(obj.name())
    return obj.name()