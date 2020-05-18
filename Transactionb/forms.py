
from django import forms
from django.forms import ModelForm
from .models import Transactionb

class TransactionForm(ModelForm):
    class Meta:
        model = Transactionb
        fields = ('Date', 'Date_transaction','validation','E_S','reference','mode_de_payement','Montant_HT','Montant_TVA','Montant_TTC','Numero_facture','Numero_payement')



class Valid(forms.Form):
    Date = forms.DateField()
    Validation = forms.CharField(max_length=200)