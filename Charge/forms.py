from django import forms
from django.forms import ModelForm
from .models import Charge
from Gestion_Achats.models import Payements
from django.forms import ValidationError

class ChargeForm(ModelForm):
    Description = forms.CharField()
    class Meta:
        model = Charge
        fields = ('Date', 'Date_limit','Etat','Montant','Description','Designation_charge')



class Payments_charge_Form(forms.ModelForm):
    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')

    def __init__(self, *args, **kwargs):
        self.charge = kwargs.pop("charge")
        super(Payments_charge_Form, self).__init__(*args, **kwargs)

        charge = Charge.objects.get(id=self.charge)
        self.initial['E_S'] = 'Dépence'
        self.initial['reference'] = charge.id
        self.initial['Montant_HT'] = charge.Montant
        self.initial['Montant_TTC'] = charge.Montant


    def clean(self):
        cleaned_data = self.cleaned_data
        Date = self.cleaned_data.get('Date')
        Date_limit = self.cleaned_data.get('Date_limit')
        Etat = self.cleaned_data.get('Etat')
        Montant = self.cleaned_data.get('Montant')
        Description = self.cleaned_data.get('Description')
        Designation_charge = self.cleaned_data.get('Designation_charge')
        Numero_facture = self.cleaned_data.get('Numero_facture')
        Numero_payement = self.cleaned_data.get('Numero_payement')
        E_S = self.cleaned_data.get('E_S')



        if Payements.objects.filter(Date=Date).exists() and Payements.objects.filter(
                Date_limit=Date_limit).exists() and Payements.objects.filter(
            Etat=Etat).exists() and Payements.objects.filter(
            Numero_facture=Numero_facture).exists() and Payements.objects.filter(
            Montant=Montant).exists() and  Payements.objects.filter(
            Designation_charge=Designation_charge).exists() and  Payements.objects.filter(
            Description=Description).exists():
            raise ValidationError('data exists ')

        return cleaned_data