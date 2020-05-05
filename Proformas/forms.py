from django import forms
from .models import Commande_Designation,Commande,Modalite
from django.forms import ModelForm


class Commande_Form(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('Date','Client','Numero_commande','Montant_HT','Montant_TVA','Montant_TTC','Type_Service','validation')



class Commande_D_Form(forms.ModelForm):
    Designation = forms.CharField()
    class Meta:

        model = Commande_Designation
        fields = ('Designation','Prix_Unitaire','Command','Quantite','Montant_HT','Montant_TVA','Montant_TTC')


class Modalite_Form(forms.ModelForm):
    modalite_payement = forms.CharField(required=False)
    Arret_Facture = forms.CharField(required=False)
    Formation = forms.CharField(required=False)
    Period_Réalisation = forms.CharField(required=False)
    Echéancier_payement = forms.CharField(required=False)
    class Meta:
        model = Modalite
        fields = ('modalite_payement','Arret_Facture','Formation','Period_Réalisation','Echéancier_payement','Command')
