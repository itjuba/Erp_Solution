from django import forms
from .models import Commande_Designation,Commande,Modalite
from django.forms import ValidationError

from django.forms import ModelForm


class Commande_Form(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('Date','Client','Numero_commande','Montant_HT','Montant_TVA','Montant_TTC','Type_Service','validation')

    def clean(self):
        cleaned_data = self.cleaned_data
        Date = self.cleaned_data.get('Date')
        Client = self.cleaned_data.get('Client')
        Numero_commande = self.cleaned_data.get('Numero_commande')
        Montant_HT = self.cleaned_data.get('Montant_HT')
        Montant_TVA = self.cleaned_data.get('Montant_TVA')
        Montant_TTC = self.cleaned_data.get('Montant_TTC')
        validation = self.cleaned_data.get('validation')

        if Commande.objects.filter(Date=Date).exists() and Commande.objects.filter(
            Client=Client).exists() and Commande.objects.filter(
            Numero_commande=Numero_commande).exists() and Commande.objects.filter(
            Montant_HT=Montant_HT).exists() and Commande.objects.filter(Montant_TVA=Montant_TVA).exists() and Commande.objects.filter(Montant_TTC=Montant_TTC).exists() and Commande.objects.filter(validation=validation).exists():
             raise ValidationError('data exists ')

        return cleaned_data

class Commande_D_Form(forms.ModelForm):
    Designation = forms.CharField(required=True)
    class Meta:

        model = Commande_Designation
        fields = ('Designation','Prix_Unitaire','Command','Quantite','Montant_HT','Montant_TVA','Montant_TTC')

    def __init__(self, *args, **kwargs):
        super(Commande_D_Form, self).__init__(*args, **kwargs)

        commande =  Commande.objects.latest('id')
        self.initial['Command'] = commande


    def clean(self):
            cleaned_data = self.cleaned_data
            Designation = self.cleaned_data.get('Designation')
            Prix_Unitaire = self.cleaned_data.get('Prix_Unitaire')
            Command = self.cleaned_data.get('Command')
            Quantite = self.cleaned_data.get('Quantite')
            Montant_HT = self.cleaned_data.get('Montant_HT')
            Montant_TVA = self.cleaned_data.get('Montant_TVA')
            Montant_TTC = self.cleaned_data.get('Montant_TTC')

            if not (Designation and Prix_Unitaire and Command and Quantite and Montant_HT and Montant_TVA and Montant_TTC):
                raise ValidationError('Check your inputs!')

            if Commande_Designation.objects.filter(Designation=Designation).exists() and Commande_Designation.objects.filter(
                Prix_Unitaire=Prix_Unitaire).exists() and Commande_Designation.objects.filter(
                Command=Command).exists()  and Commande_Designation.objects.filter(
                Quantite=Quantite).exists() and Commande_Designation.objects.filter(
                Montant_HT=Montant_HT).exists() and Commande_Designation.objects.filter(
                Montant_TVA=Montant_TVA).exists() and Commande_Designation.objects.filter(
                Montant_TTC=Montant_TTC).exists():
                 raise ValidationError('data exists ')

            return cleaned_data

class Modalite_Form(forms.ModelForm):
    modalite_payement = forms.CharField(required=False)
    Arret_Facture = forms.CharField(required=False)
    Formation = forms.CharField(required=False)
    Period_Réalisation = forms.CharField(required=False)
    Echéancier_payement = forms.CharField(required=False)
    class Meta:
        model = Modalite
        fields = ('modalite_payement','Arret_Facture','Formation','Period_Réalisation','Echéancier_payement','Command')

    def __init__(self, *args, **kwargs):
        super(Modalite_Form, self).__init__(*args, **kwargs)

        commande = Commande.objects.latest('id')
        self.initial['Command'] = commande
    def clean(self):
        cleaned_data = self.cleaned_data
        modalite_payement = self.cleaned_data.get('modalite_payement')
        Arret_Facture = self.cleaned_data.get('Arret_Facture')
        Formation = self.cleaned_data.get('Formation')
        Period_Réalisation = self.cleaned_data.get('Period_Réalisation')
        Echéancier_payement = self.cleaned_data.get('Echéancier_payement')
        Command = self.cleaned_data.get('Command')


        if Modalite.objects.filter(modalite_payement=modalite_payement).exists() and Modalite.objects.filter(
            modalite_payement=modalite_payement).exists() and Modalite.objects.filter(
            Arret_Facture=Arret_Facture).exists() and Modalite.objects.filter(
            Formation=Formation).exists() and Modalite.objects.filter(
            Echéancier_payement=Echéancier_payement).exists() and Modalite.objects.filter(
            Command=Command).exists():
             raise ValidationError('data exists ')

        return cleaned_data