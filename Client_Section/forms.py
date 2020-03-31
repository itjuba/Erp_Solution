from django import forms
from .models import Client_Data

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client_Data
        fields = ('id', 'Name', 'RC', 'tel', 'fax', 'adresse', 'active' ,)