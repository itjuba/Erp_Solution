
from django import forms
from django.forms import ModelForm
from .models import Transactionb

class TransactionForm(ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    Date_transaction = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Transactionb
        fields = ('Date', 'Date_transaction','validation','E_S','reference','mode_de_payement','Montant_HT','Montant_TVA','Montant_TTC','Numero_facture','Numero_payement')



class Valid(forms.Form):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    Validation = forms.CharField(max_length=200)