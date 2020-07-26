from django.contrib import admin
from .models import Client_Data,Contact

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('RC', 'Raison_social', 'NIF','AI','NIS','Banque','CB','adresse','active')
    search_fields = ('Raison_social',)

    site_url = 'https://localhost:8000/home'


admin.site.register(Client_Data,ClientAdmin)
admin.site.register(Contact)