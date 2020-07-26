from django.contrib import admin
from .models import Fournis_Data,Fournis_Contact

# Register your models here.



class FournisAdmin(admin.ModelAdmin):
    list_display = ('RC', 'Raison_social', 'NIF','AI','NIS','Banque','CB','adresse','active')
    search_fields = ('Raison_social',)



admin.site.register(Fournis_Data,FournisAdmin)
admin.site.register(Fournis_Contact)