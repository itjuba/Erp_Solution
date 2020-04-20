from django import forms
from django.forms import ModelForm
from .models import Achats,Article,Association
from django.forms.models import BaseModelFormSet


class AchatForm(ModelForm):
    class Meta:
        model = Achats
        fields = ('Date','Id_Fournis','Montant_HT','Montant_TVA','Montant_TTC')



class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Designation','Code','Description','Service')


class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ('Id_Achats', 'Id_Article', 'Prix_Unitaire', 'Quantite')

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.queryset = Association.objects.none()








