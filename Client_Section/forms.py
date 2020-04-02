from django import forms
from .models import Client_Data

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client_Data
        fields = ('id', 'RC','Raison_social','NIF','AI','NIS','CB','Banque', 'adresse', 'active' ,)