from django import forms
from django.forms import ModelForm
from .models import Achats,Article,Association,Payements
from django.forms.models import BaseModelFormSet
from django.forms import modelformset_factory
from django.forms import ValidationError
from Charge.models import Charge
from django.shortcuts import get_object_or_404

from django.db.models import Sum

TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'
ORDERING_FIELD_NAME = 'ORDER'
DELETION_FIELD_NAME = 'DELETE'

# default minimum number of forms in a formset
DEFAULT_MIN_NUM = 0

# default maximum number of forms in a formset, to prevent memory exhaustion
DEFAULT_MAX_NUM = 1000


class AchatForm(ModelForm):
    # Date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_HT = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_TVA = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_pay = forms.DecimalField(required=False)
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = Achats
        fields = ('Date','Id_Fournis','Montant_HT','Montant_TVA','Montant_TTC','Montant_pay')

    def clean(self):
        cleaned_data = self.cleaned_data
        Date = self.cleaned_data.get('Date')
        Id_Fournis = self.cleaned_data.get('Id_Fournis')
        Montant_HT = self.cleaned_data.get('Montant_HT')
        Montant_TVA = self.cleaned_data.get('Montant_TVA')
        Montant_TTC = self.cleaned_data.get('Montant_TTC')

        # if Achats.objects.filter(Date=Date).exists() and Achats.objects.filter(
        #         Id_Fournis=Id_Fournis).exists() and Achats.objects.filter(
        #         Montant_HT=Montant_HT).exists() and Achats.objects.filter(
        #         Montant_TVA=Montant_TVA).exists() and Achats.objects.filter(Montant_TTC=Montant_TTC).exists():
        #     # {'error': [ValidationError([u'Data Exist !.']},
        #     raise ValidationError('data exists ')

        return cleaned_data

class AchatForm2(ModelForm):
    # Date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_HT = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_TVA = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    Montant_pay = forms.DecimalField(required=False)
    class Meta:
        model = Achats
        fields = ('Date','Montant_HT','Montant_TVA','Montant_TTC','Montant_pay')







class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Designation','Code','Description','Service')

class AssociationForm3(forms.ModelForm):
    # Id_Achats = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Quantite = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Association
        fields = ('Id_Achats', 'Id_Article', 'Prix_Unitaire', 'Quantite')

    def __init__(self, *args, **kwargs):
        super(AssociationForm3, self).__init__(*args, **kwargs)
        self.fields['Id_Achats'].widget.attrs['class'] = 'form-control';
        self.fields['Id_Article'].widget.attrs['class'] = 'form-control';




class AssociationForm(forms.ModelForm):
    Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    Quantite = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Association
        fields = ('Id_Achats', 'Id_Article', 'Prix_Unitaire', 'Quantite')

    def __init__(self, *args, **kwargs):
        self.achats = kwargs.pop("achats")
        print(self.achats)
        super(AssociationForm, self).__init__(*args, **kwargs)


        self.fields['Id_Achats'].widget.attrs['class'] = 'form-control';
        self.fields['Id_Article'].widget.attrs['class'] = 'form-control';
        self.initial['Id_Achats'] = self.achats

    def clean(self):
        cleaned_data = self.cleaned_data
        Id_Achats = self.cleaned_data.get('Id_Achats')
        Id_Article = self.cleaned_data.get('Id_Article')
        Prix_Unitaire = self.cleaned_data.get('Prix_Unitaire')
        Quantite = self.cleaned_data.get('Quantite')




        # for x in Quantite :
        #     print(x)

        # if not (Id_Achats and Id_Article and Prix_Unitaire and Quantite):
        #     raise ValidationError('Check your inputs !')



        # if Association.objects.filter(Id_Achats=Id_Achats).exists() and Association.objects.filter(
        #         Id_Article=Id_Article).exists() and Association.objects.filter(
        #         Prix_Unitaire=Prix_Unitaire).exists() and Association.objects.filter(
        #         Quantite=Quantite).exists():
        #     raise ValidationError('data exists ')

        return cleaned_data



form = modelformset_factory(Association, form=AssociationForm, extra=5)

form = modelformset_factory(Association, form=AssociationForm, extra=5,can_delete=True)
class AssociationForm2(forms.ModelForm):
    # Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class': 'na'}))
    # Quantite = forms.CharField(widget=forms.TextInput(attrs={'class': 'qu'}))
    class Meta:
        model = Association
        fields = ('Id_Achats', 'Id_Article', 'Prix_Unitaire', 'Quantite')



    def __init__(self, *args, **kwargs):
        super(AssociationForm2, self).__init__(*args, **kwargs)


        self.initial['Id_Achats'] = Achats.objects.latest('id')
        self.fields['Prix_Unitaire'].widget.attrs['class'] = 'na form-control';
        self.fields['Id_Article'].widget.attrs['class'] = 'form-control';
        self.fields['Quantite'].widget.attrs['class'] = 'qu l form-control'
        self.fields['Id_Achats'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = self.cleaned_data
        Id_Achats = self.cleaned_data.get('Id_Achats')
        print(Id_Achats)
        Id_Article = self.cleaned_data.get('Id_Article')
        print(Id_Article)
        Prix_Unitaire = self.cleaned_data.get('Prix_Unitaire')
        print(Prix_Unitaire)

        Quantite = self.cleaned_data.get('Quantite')
        print(Quantite)


        if not ( Id_Article and Prix_Unitaire and Quantite):
            raise ValidationError('Form Invalide nadjib!')

        if Id_Article == None:
            print('not')
            raise ValidationError('not !')


        return cleaned_data
class Payments_Form2(forms.ModelForm):
    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')



class Payments_Form(forms.ModelForm):
    Date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')

    def __init__(self, *args, **kwargs):
        self.form_achat_id = kwargs.pop("achat_id")
        super(Payments_Form, self).__init__(*args, **kwargs)
        if Achats.objects.get(id=self.form_achat_id):
         achat = Achats.objects.get(id=self.form_achat_id)
        else :
          charge = Charge.objects.get(id=self.form_achat_id)
        self.initial['E_S'] = 'Dépence'
        self.initial['reference'] = achat.id
        self.initial['Montant_HT'] = achat.Montant_HT
        self.initial['Montant_TVA'] = achat.Montant_HT
        self.initial['Montant_TTC'] = achat.Montant_HT

    def clean(self):
        cleaned_data = self.cleaned_data
        Date = self.cleaned_data.get('Date')
        reference = self.cleaned_data.get('reference')
        mode_de_payement = self.cleaned_data.get('mode_de_payement')
        Montant_HT = self.cleaned_data.get('Montant_HT')
        Montant_TVA = self.cleaned_data.get('Montant_TVA')
        Montant_TTC = self.cleaned_data.get('Montant_TTC')
        Numero_facture = self.cleaned_data.get('Numero_facture')
        Numero_payement = self.cleaned_data.get('Numero_payement')
        E_S = self.cleaned_data.get('E_S')



        if Payements.objects.filter(Date=Date).exists() and Payements.objects.filter(
                reference=reference).exists() and Payements.objects.filter(
            mode_de_payement=mode_de_payement).exists() and Payements.objects.filter(
            Numero_facture=Numero_facture).exists() and Payements.objects.filter(
            Montant_HT=Montant_HT).exists() and  Payements.objects.filter(
            Montant_TTC=Montant_TTC).exists() and  Payements.objects.filter(
            Montant_TVA=Montant_TVA).exists() and  Payements.objects.filter(
            Numero_payement=Numero_payement).exists() and  Payements.objects.filter(
            Montant_TTC=Montant_TTC).exists() and  Payements.objects.filter(
            Numero_payement=Numero_payement).exists() and Payements.objects.filter(E_S=E_S).exists():
            raise ValidationError('data exists ')

        return cleaned_data



