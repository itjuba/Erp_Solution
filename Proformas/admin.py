from django.contrib import admin

from .models import Commande,Modalite,Commande_Designation,Facture


admin.site.register(Commande)
admin.site.register(Commande_Designation)
admin.site.register(Modalite)
admin.site.register(Facture)

