from django import forms
from django.forms import ModelForm
from .models import Achats,Article,Association
from django.forms.models import BaseModelFormSet
from django.forms import modelformset_factory
from django.forms import ValidationError


class AchatForm(ModelForm):
    # Date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_HT = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_TVA = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Montant_TTC = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Achats
        fields = ('Date','Id_Fournis','Montant_HT','Montant_TVA','Montant_TTC')

    def clean(self):
        cleaned_data = self.cleaned_data
        Date = self.cleaned_data.get('Date')
        Id_Fournis = self.cleaned_data.get('Id_Fournis')
        Montant_HT = self.cleaned_data.get('Montant_HT')
        Montant_TVA = self.cleaned_data.get('Montant_TVA')
        Montant_TTC = self.cleaned_data.get('Montant_TTC')

        if Achats.objects.filter(Date=Date).exists() and  Achats.objects.filter(Id_Fournis=Id_Fournis).exists() and  Achats.objects.filter(Montant_HT=Montant_HT).exists():
            raise ValidationError('data exists ')

        return cleaned_data




class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Designation','Code','Description','Service')


class AssociationForm(forms.ModelForm):
    # Prix_Unitaire = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Quantite = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Association
        fields = ('Id_Achats', 'Id_Article', 'Prix_Unitaire', 'Quantite')

    # def __init__(self, *args, **kwargs):
    #     super(AssociationForm, self).__init__(*args, **kwargs)
    #     self.queryset = Association.objects.none()

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.initial['Id_Achats'] = Achats.objects.latest('id')


form = modelformset_factory(Association, form=AssociationForm, extra=5)



