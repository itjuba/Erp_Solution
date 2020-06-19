from django import forms
from django.forms import ModelForm
from .models import Charge
from Gestion_Achats.models import Payements
from django.forms import ValidationError

class ChargeForm(ModelForm):
    Description = forms.CharField()
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = Charge
        fields = ('Date', 'Date_limit','Montant','Description','Designation_charge')

    def __init__(self, *args, **kwargs):
        super(ChargeForm, self).__init__(*args, **kwargs)

        self.initial['Etat'] = False

class Payments_charge_Form(forms.ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')

    def __init__(self, *args, **kwargs):
        self.charge = kwargs.pop("charge")
        super(Payments_charge_Form, self).__init__(*args, **kwargs)

        charge = Charge.objects.get(id=self.charge)
        self.initial['E_S'] = 'Charge'
        self.initial['Montant_TVA'] = 0
        self.initial['reference'] = charge.id
        self.initial['Montant_HT'] = charge.Montant
        self.initial['Montant_TTC'] = charge.Montant


    def clean(self):
        cleaned_data = self.cleaned_data
        Date = self.cleaned_data.get('Date')
        Montant_HT = self.cleaned_data.get('Montant_HT')
        Montant_TVA = self.cleaned_data.get('Montant_TVA')
        Montant_TTC = self.cleaned_data.get('Montant_TTC')
        E_S = self.cleaned_data.get('E_S')
        reference = self.cleaned_data.get('reference')
        Numero_payement = self.cleaned_data.get('Numero_payement')
        mode_de_payement = self.cleaned_data.get('mode_de_payement')




        if Payements.objects.filter(Date=Date).exists() and Payements.objects.filter(
            Montant_HT=Montant_HT).exists() and Payements.objects.filter(Montant_TVA=Montant_TVA) and Payements.objects.filter(Montant_TTC=Montant_TTC) and Payements.objects.filter(
            E_S=E_S).exists() and Payements.objects.filter(
            reference=reference).exists() and  Payements.objects.filter(
            Numero_payement=Numero_payement).exists() and  Payements.objects.filter(
            mode_de_payement=mode_de_payement).exists():
            raise ValidationError('data exists ')

        return cleaned_data