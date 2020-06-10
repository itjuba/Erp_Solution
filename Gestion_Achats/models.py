from django.db import models
from enum import Enum
from Fournis_Section.models import Fournis_Data
from Proformas.models import Facture
from Charge.models import Charge
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
         return str(self.id)

   def name(self):
      return str(self.Id_Fournis.Raison_social)


class Association(models.Model):
   Id_Achats = models.ForeignKey(Achats, on_delete=models.CASCADE)
   Id_Article = models.ForeignKey(Article,on_delete=models.CASCADE,null=False,blank=False)
   Prix_Unitaire = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
   Quantite = models.IntegerField(null=False,blank=False)

   def __str__(self):
      return str(self.Id_Achats)

   # @property
   # def total_cost(self):
   #    return self.Prix_Unitaire * self.Quantite



class Payements(models.Model):

   class Payement_Choic(models.TextChoices):
      Chéque = "Chéque"
      espèces = "espèces"
      virement = "virement bancaire"

   Date = models.DateField()
   E_S = models.CharField(max_length=10)
   mode_de_payement = models.CharField(choices=Payement_Choic.choices,max_length=200)
   reference = models.IntegerField()
   Montant_HT = models.DecimalField(max_digits=10, decimal_places=2)
   Montant_TVA = models.DecimalField(max_digits=10, decimal_places=2)
   Montant_TTC = models.DecimalField(max_digits=10, decimal_places=2)
   Numero_facture = models.IntegerField()
   Numero_payement =  models.IntegerField()

   def  __str__(self):
     return str(self.Date)

   def name(self):
      if Charge.objects.filter(id=self.reference).exists():
         charge = Charge.objects.get(id=self.reference)
         return str(charge.Description)

      elif  Achats.objects.filter(id=self.reference).exists():
         payement = Achats.objects.get(id=self.reference)
         if payement.Id_Fournis:
          return str(payement.Id_Fournis)
         else:
            return str(payement.Date)


      elif Facture.objects.filter(commande=self.reference).exists():
         print('yes')
         facture =  Facture.objects.get(commande=self.reference)
         return str(facture.__str__())
      else:
         return self.reference