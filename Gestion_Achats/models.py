from django.db import models
from enum import Enum
from Fournis_Section.models import Fournis_Data
# Create your models here.

from django.shortcuts import get_object_or_404

class Article(models.Model):
   Designation  = models.CharField(max_length=200)
   Code   =   models.CharField(max_length=200)
   Description = models.CharField(max_length=200)
   Service  = models.BooleanField()

   def __str__(self):
      return self.Description


class Achats(models.Model):
   Date = models.DateField()
   Id_Fournis = models.ForeignKey(Fournis_Data, blank=True, on_delete=models.CASCADE)
   Montant_HT = models.DecimalField(max_digits=10,decimal_places=2)
   Montant_TVA = models.DecimalField(max_digits=10,decimal_places=2)
   Montant_TTC = models.DecimalField(max_digits=10,decimal_places=2)
   Montant_pay =  models.DecimalField(max_digits=10,decimal_places=2,default=0)

   def __str__(self):
         return str(self.Id_Fournis.Raison_social)


class Association(models.Model):
   Id_Achats = models.ForeignKey(Achats, blank=True, on_delete=models.CASCADE)
   Id_Article = models.ForeignKey(Article, blank=True, on_delete=models.CASCADE)
   Prix_Unitaire = models.DecimalField(max_digits=10,decimal_places=2,default=0)
   Quantite = models.IntegerField(default=1,blank=False,null=False)

   def __str__(self):
      return str(self.Id_Article)

   # @property
   # def total_cost(self):
   #    return self.Prix_Unitaire * self.Quantite



class Payements(models.Model):

   class Payement_Choic(models.TextChoices):
      Chéck = "Chéck"
      espèces = "espèces"
      virement = "par virement bancaire"

   Date = models.DateField()
   E_S = models.CharField(max_length=10)
   mode_de_payement = models.CharField(choices=Payement_Choic.choices,max_length=200)
   reference = models.IntegerField()
   Montant_HT = models.DecimalField(max_digits=10, decimal_places=2)
   Montant_TVA = models.DecimalField(max_digits=10, decimal_places=2)
   Montant_TTC = models.DecimalField(max_digits=10, decimal_places=2)
   Numero_facture = models.IntegerField()
   Numero_payement =  models.IntegerField()



   def __str__(self):
      payement = get_object_or_404(Achats, pk=self.reference)
      return str(payement.Id_Fournis)