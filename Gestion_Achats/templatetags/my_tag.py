from django.template import Library

register = Library()


@register.filter
def achat(obj):
    print(obj.__str__())
    return obj.__str__()