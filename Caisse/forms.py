from django import forms
from django.forms import ModelForm
from .models import Caisse
from django.forms import ValidationError




class Caisse_Form(ModelForm):
    Nature = forms.CharField()
    class Meta:
        model = Caisse
        fields = ('ES', 'Date','Nature','Montant')

    def __init__(self, *args, **kwargs):
        super(Caisse_Form, self).__init__(*args, **kwargs)

