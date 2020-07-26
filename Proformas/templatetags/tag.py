from django.template import Library
from ..admin import Facture

register = Library()


@register.filter
def filter(obj):
   if Facture.objects.filter(commande=obj.id).exists():

     return False;
   else:
       return True


