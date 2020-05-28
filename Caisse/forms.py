from django import forms
from django.forms import ModelForm
from .models import Caisse
from Transactionb.models import  Transactionb

from django.forms import ValidationError




class Caisse_Form(ModelForm):
    Nature = forms.CharField()
    class Meta:
        model = Caisse
        fields = ('ES', 'Date','Nature','Montant')

    def __init__(self, *args, **kwargs):
        super(Caisse_Form, self).__init__(*args, **kwargs)



class TransactionForm(ModelForm):
    class Meta:
        model = Transactionb
        fields = ('Date', 'Date_transaction','validation','E_S','reference','mode_de_payement','Montant_HT','Montant_TVA','Montant_TTC','Numero_facture','Numero_payement')

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.initial['mode_de_payement'] ="Chéque"
        self.initial['Numero_facture'] = ""
        self.initial['E_S'] = "E"
        self.fields['reference'].required = False
        self.fields['Numero_facture'].required = False

