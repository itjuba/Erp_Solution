from django.template import Library

register = Library()


@register.simple_tag()
def multiply(prix, quan, *args, **kwargs):
    # you would need to do any localization of the result here
    return prix * quan