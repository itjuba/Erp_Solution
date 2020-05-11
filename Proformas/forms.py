from django import forms
from .models import Commande_Designation,Commande,Modalite,Facture
from django.forms import ValidationError
from Gestion_Achats.models import Payements


from django.forms import ModelForm
class Payments_Form_facture(forms.ModelForm):
    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')

    def __init__(self, *args, **kwargs):
        self.facture = kwargs.pop("facture")
        super(Payments_Form_facture, self).__init__(*args, **kwargs)

        facture = Facture.objects.get(id=self.facture)
        self.initial['E_S'] = 'Vente'
        self.initial['reference'] = facture.id
        self.initial['Montant_HT'] = facture.Montant_HT
        self.initial['Montant_TVA'] = facture.Montant_TVA
        self.initial['Montant_TTC'] = facture.Montant_TTC
        self.initial['Numero_facture'] = facture.Montant_TTC



class Facture_Form(forms.ModelForm):
    Titre_facture = forms.CharField()
    class Meta:
        model = Facture
        fields = ('Date','Etat','commande','Titre_facture','Numero_facture','Montant_HT','Montant_TVA','Montant_TTC','Date_limite_payement')

    def __init__(self, *args, **kwargs):
        self.fac = kwargs.pop("fac")
        super(Facture_Form, self).__init__(*args, **kwargs)
        com = self.fac
        # commande = Facture.objects.get(id=self.fac)
        com = Commande.objects.get(id=self.fac)
        self.initial['commande'] = com

    def clean(self):
        cleaned_data = self.cleaned_data
        Montant_TTC = self.cleaned_data.get('Montant_TTC')
        commande = self.cleaned_data.get('commande')
        command = Commande.objects.get(id=commande.id)
        ttc= command.Montant_TTC
        if Montant_TTC > ttc:
            raise ValidationError('KBIR')


class Commande_Form2(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('Date','Client','Numero_commande','Montant_HT','Montant_TVA','Montant_TTC','Type_Service','validation','Date_validation')


class Commande_Form(forms.ModelForm):

    class Meta:
        model = Commande
        fields = ('Date','Client','Numero_commande','Montant_HT','Montant_TVA','Montant_TTC','Type_Service','validation','Date_validation')

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
    Debut_realsiation = forms.CharField(required=False)
    Garantie = forms.CharField(required=False)
    class Meta:
        model = Modalite
        fields = ('modalite_payement','Arret_Facture','Formation','Period_Réalisation','Echéancier_payement','Debut_realsiation','Garantie','Formation','Command')

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



class validat(forms.Form):
    Validate_date = forms.DateField()
