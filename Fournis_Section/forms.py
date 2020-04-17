from django import forms
from django.forms import ModelForm
from .models import Fournis_Data,Fournis_Contact


class FournisForm(ModelForm):
    class Meta:
        model = Fournis_Data
        fields = ('id', 'RC','Raison_social','NIF','AI','NIS','CB','Banque', 'adresse', 'active',)





class Contact_Fournis_Form(forms.ModelForm):
    class Meta:
        model = Fournis_Contact
        fields = ('Nom','post','Tel','email','contact_type','Fournis')

    def __init__(self,*args, **kwargs):
        super(Contact_Fournis_Form, self).__init__(*args, **kwargs)
        self.fields['Fournis'].queryset = Fournis_Data.objects.all()