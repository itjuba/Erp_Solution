from django.template import Library
from Gestion_Achats.models import Payements
import datetime
register = Library()


@register.filter
def edit(obj):
    if Payements.objects.filter(reference=obj.reference).exists():
        # print("true")
        return True
    else:
        # print('false')
        return False