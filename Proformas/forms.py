from django import forms
from .models import Commande_Designation,Commande,Modalite,Facture
from django.forms import ValidationError
from Gestion_Achats.models import Payements
from django.shortcuts import render,get_object_or_404,HttpResponse,HttpResponseRedirect



from django.forms import ModelForm
class Payments_Form_facture(forms.ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')

    def __init__(self, *args, **kwargs):
        self.facture = kwargs.pop("facture")
        print(self.facture)
        super(Payments_Form_facture, self).__init__(*args, **kwargs)
        facture = Facture.objects.get(id=self.facture)
        print(facture.commande)
        self.initial['E_S'] = 'Vente'
        self.initial['reference'] = facture.commande_id
        self.initial['Montant_HT'] = facture.Montant_HT
        self.initial['Montant_TVA'] = facture.Montant_TVA
        self.initial['Montant_TTC'] = facture.Montant_TTC
        self.initial['Numero_facture'] = facture.Numero_facture

    def clean(self):
        idp = self.facture
        fac = get_object_or_404(Facture,id=idp)
        print(fac.commande_id)
        print(idp)
        pay = Payements.objects.filter(reference=fac.commande_id)
        if pay:
            raise ValidationError('le payement de cette facture exist deja !')


class Facture_Form2(forms.ModelForm):
    Titre_facture = forms.CharField()
    Date =  forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    Date_limite_payement =  forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    Date_payement = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}),required=False)
    class Meta:
        model = Facture
        fields = ('Date','commande','Titre_facture','Numero_facture','Montant_HT','Montant_TVA','Montant_TTC','Date_limite_payement','Date_payement')


class Facture_Form(forms.ModelForm):
    Date =  forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    Date_limite_payement =  forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    #Date_payement = forms.CharField(widget=forms.TextInput(attrs={'type':'date'}))
    Titre_facture = forms.CharField()
    class Meta:
        model = Facture
        fields = ('Date','Etat','commande','Titre_facture','Numero_facture','Montant_HT','Montant_TVA','Montant_TTC','Date_limite_payement')

    def __init__(self, *args, **kwargs):
        self.fac = kwargs.pop("fac")
        super(Facture_Form, self).__init__(*args, **kwargs)
        com = self.fac
        print(com)
        commande = get_object_or_404(Commande,id=self.fac)

        # if get_object_or_404(Facture,id=com):
        #   facture = get_object_or_404(Facture,id=com)
        #   commande = get_object_or_404(Commande,id=facture.commande_id)

        com = Commande.objects.get(id=self.fac)
        self.initial['commande'] = com
        self.initial['Montant_HT'] = commande.Montant_HT
        self.initial['Montant_TTC'] = com.Montant_TTC
        self.initial['Montant_TVA'] = com.Montant_TVA




    def clean(self):
        cleaned_data = self.cleaned_data
        Montant_TTC = self.cleaned_data.get('Montant_TTC')
        commande = self.cleaned_data.get('commande')
        command = Commande.objects.get(id=commande.id)
        print(commande.id)
        if Facture.objects.filter(commande=commande.id).exists():
            raise ValidationError('il existe une facture pour cette commande !')
        ttc= command.Montant_TTC
        # if Montant_TTC > ttc:
        #     raise ValidationError('le montant ttc facture > montant ttc commmande ')

class Commande_Formna(forms.ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    #Date_validation = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Commande
        fields = ('Date','Client','Numero_commande','Montant_HT','Montant_TVA','Montant_TTC','Type_Service','validation','Date_validation')

   


class Commande_Form2(forms.ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    Date_validation = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Commande
        fields = ('Date','Client','Numero_commande','Montant_HT','Montant_TVA','Montant_TTC','Type_Service','validation','Date_validation')


class Commande_Form_step(forms.ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Commande
        fields = ('Date','Client','Numero_commande','Montant_HT','Montant_TVA','Montant_TTC','Type_Service')

    def clean(self):
        cleaned_data = self.cleaned_data
        Date = self.cleaned_data.get('Date')
        Client = self.cleaned_data.get('Client')
        Numero_commande = self.cleaned_data.get('Numero_commande')
        Montant_HT = self.cleaned_data.get('Montant_HT')
        Montant_TVA = self.cleaned_data.get('Montant_TVA')
        Montant_TTC = self.cleaned_data.get('Montant_TTC')
       

        if not (Date and Client and Numero_commande and Montant_HT and Montant_HT  and Montant_TTC ):
            raise ValidationError('verifier les champs vide de la commande ! ')

        return cleaned_data

class Commande_Form(forms.ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    Date_validation = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
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

        # if Commande.objects.filter(Date=Date).exists() and Commande.objects.filter(
        #     Client=Client).exists() and Commande.objects.filter(
        #     Numero_commande=Numero_commande).exists() and Commande.objects.filter(
        #     Montant_HT=Montant_HT).exists() and Commande.objects.filter(Montant_TVA=Montant_TVA).exists() and Commande.objects.filter(Montant_TTC=Montant_TTC).exists() and Commande.objects.filter(validation=validation).exists():
        #      raise ValidationError('data exists ')

        return cleaned_data


class Commande_D_Form2(forms.ModelForm):
    Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class': 'na form-control'}))
    Quantite = forms.CharField(widget=forms.TextInput(attrs={'class': 'qu l form-control'}))
    Montant_HT = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_TVA = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_TTC = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Designation = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Commande_Designation
        fields = ('Designation','Prix_Unitaire','Command','Quantite','Montant_HT','Montant_TVA','Montant_TTC')

    def __init__(self, *args, **kwargs):
        self.com = kwargs.pop('com')
        print(self.com)
        super(Commande_D_Form2, self).__init__(*args, **kwargs)
        self.initial['Command'] = self.com
        self.fields['Command'].widget.attrs['class'] = 'form-control';
        self.fields['Montant_HT'].required = False
        self.fields['Montant_TVA'].required = False
        self.fields['Montant_TTC'].required = False



class Commande_D_Form_p(forms.ModelForm):
    Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class': 'na form-control'}))
    #Command = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    Quantite = forms.CharField(widget=forms.TextInput(attrs={'class': 'qu l form-control'}))
    Montant_HT = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_TVA = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_TTC = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Designation = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = Commande_Designation
        fields = ('Designation','Prix_Unitaire','Command','Quantite','Montant_HT','Montant_TVA','Montant_TTC')

    def __init__(self, *args, **kwargs):
        self.com = kwargs.pop('com')
        print(self.com)
        super(Commande_D_Form_p, self).__init__(*args, **kwargs)
        self.initial['Command'] = self.com
        self.fields['Command'].widget.attrs['class'] = 'form-control';
        self.fields['Montant_HT'].required = False
        self.fields['Montant_TVA'].required = False
        self.fields['Montant_TTC'].required = False




class Commande_D_Form(forms.ModelForm):
    Designation = forms.CharField(required=True)
    Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class': 'na form-control'}))
    Quantite = forms.CharField(widget=forms.TextInput(attrs={'class': 'qu l form-control'}))
    Montant_HT = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_TVA = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_TTC = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Designation = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Commande_Designation
        fields = ('Designation','Prix_Unitaire','Command','Quantite','Montant_HT','Montant_TVA','Montant_TTC')

    def __init__(self, *args, **kwargs):
        super(Commande_D_Form, self).__init__(*args, **kwargs)


        self.initial['Command'] = Commande.objects.latest('id')
       
        
        self.fields['Command'].widget = forms.HiddenInput()
        self.fields['Command'].required = False

        self.fields['Montant_HT'].required = False
        self.fields['Montant_TVA'].required = False
        self.fields['Montant_TTC'].required = False

    def save(self,commit=True):
        commande =  super(Commande_D_Form, self).save(commit = False)
        commande.Command = Commande.objects.latest('id')
        commande.save()
        return commande



    def clean(self):
            cleaned_data = self.cleaned_data
            Designation = self.cleaned_data.get('Designation')
            Prix_Unitaire = self.cleaned_data.get('Prix_Unitaire')
            Command = self.cleaned_data.get('Command')
            Quantite = self.cleaned_data.get('Quantite')
            Montant_HT = self.cleaned_data.get('Montant_HT')
            Montant_TVA = self.cleaned_data.get('Montant_TVA')
            Montant_TTC = self.cleaned_data.get('Montant_TTC')
            Command = self.cleaned_data.get('Command')
            print(Commande)

            print(cleaned_data)

            if not (Designation and Prix_Unitaire  and Quantite):
                raise ValidationError('Check your inputs!')

            # if Commande_Designation.objects.filter(Designation=Designation).exists() and Commande_Designation.objects.filter(
            #     Prix_Unitaire=Prix_Unitaire).exists() and Commande_Designation.objects.filter(
            #     Command=Command).exists()  and Commande_Designation.objects.filter(
            #     Quantite=Quantite).exists() and Commande_Designation.objects.filter(
            #     Montant_HT=Montant_HT).exists() and Commande_Designation.objects.filter(
            #     Montant_TVA=Montant_TVA).exists() and Commande_Designation.objects.filter(
            #     Montant_TTC=Montant_TTC).exists():
            #      print('data exists')
            #      raise ValidationError('data exists ')

            return cleaned_data

class Modalite_Form(forms.ModelForm):
    modalite_payement = forms.CharField(required=False)
    Arret_Facture = forms.CharField(required=False)
    Formation = forms.CharField(required=False)
    Period_Réalisation = forms.CharField(required=False)
    Echéancier_payement = forms.CharField(required=False)

    Debut_realsiation = forms.CharField(widget=forms.TextInput(attrs={'type': 'date','requied':'false'}))

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
    Validate_date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    # Date_validation = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    # Validate_date = forms.DateField()
