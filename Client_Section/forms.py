from django import forms
from django.forms import ModelForm
from .models import Client_Data,Contact

class ClientForm(ModelForm):
    contact = forms.ModelChoiceField(queryset=Contact.objects.all())
    class Meta:
        model = Client_Data
        fields = ('id', 'RC','Raison_social','NIF','AI','NIS','CB','Banque', 'adresse', 'active','contact',)

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        contact = self.initial.get('contact')
        if contact:
            self.fields['contact'].queryset = contact.Variants.all()





class Contact_Form(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('Nom','post','Tel','email','contact_type','client')

    def __init__(self, cl,*args, **kwargs):
        super(Contact_Form, self).__init__(*args, **kwargs)
        client = self.initial.get('client')
        if client:
            self.fields['client'].queryset = Client_Data.objects.all()