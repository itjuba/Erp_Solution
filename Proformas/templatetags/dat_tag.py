from django.template import Library
import datetime
register = Library()


@register.filter
def date(obj):
    if (obj.Date_limite_payement - datetime.date.today()).days <= 5 and obj.Etat == False:
        return 'Not Payed'
    else :
        return False