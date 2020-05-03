from django import forms
from django.forms import ModelForm
from .models import Achats,Article,Association,Payements
from django.forms.models import BaseModelFormSet
from django.forms import modelformset_factory
from django.forms import ValidationError
from django.db.models import Sum

class AchatForm(ModelForm):
    # Date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_HT = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_TVA = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_pay = forms.DecimalField(required=False)
    class Meta:
        model = Achats
        fields = ('Date','Id_Fournis','Montant_HT','Montant_TVA','Montant_TTC','Montant_pay')

class AchatForm2(ModelForm):
    # Date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_HT = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_TVA = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    Montant_pay = forms.DecimalField(required=False)
    class Meta:
        model = Achats
        fields = ('Date','Montant_HT','Montant_TVA','Montant_TTC','Montant_pay')







class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Designation','Code','Description','Service')


class AssociationForm(forms.ModelForm):
    # Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class':'na'}))
    # Quantite = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Association
        fields = ('Id_Achats', 'Id_Article', 'Prix_Unitaire', 'Quantite')

    # def __init__(self, *args, **kwargs):
    #     super(AssociationForm, self).__init__(*args, **kwargs)
    #     self.queryset = Association.objects.none()

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        # self.initial['Id_Achats'] = Achats.objects.latest('id')



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
        self.fields['Prix_Unitaire'].widget.attrs['class'] = 'na';
        self.fields['Quantite'].widget.attrs['class'] = 'qu'


class Payments_Form2(forms.ModelForm):
    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')



class Payments_Form(forms.ModelForm):
    class Meta:
        model = Payements
        fields = ('Date', 'mode_de_payement', 'reference', 'Montant_HT','Montant_TVA','Montant_TTC', 'Numero_facture', 'Numero_payement','E_S')

    def __init__(self, *args, **kwargs):
        self.form_achat_id = kwargs.pop("achat_id")
        super(Payments_Form, self).__init__(*args, **kwargs)

        achat = Achats.objects.get(id=self.form_achat_id)
        self.initial['reference'] = achat.id
        self.initial['Montant_HT'] = achat.Montant_HT

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     Montant_HT = self.cleaned_data.get('Montant_HT')
    #     Montant_TTC = self.cleaned_data.get('Montant_TTC')
    #     total = Montant_TTC - Montant_HT
    #     if total<0:
    #         Montant_pay = achat.Montant_pay
    #         raise ValidationError(' rak depsit montant_ht ta3k ')








