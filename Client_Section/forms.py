from django import forms
from .models import Client_Data,Contact

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client_Data
        fields = ('id', 'RC','Raison_social','NIF','AI','NIS','CB','Banque', 'adresse', 'active' ,)






class Contact_Form(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('Nom','post','Tel','email','contact_type',)