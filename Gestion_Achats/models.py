from django.db import models

from Fournis_Section.models import Fournis_Data
# Create your models here.



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

   def __str__(self):
         return str(self.Id_Fournis.Raison_social)


class Association(models.Model):
   Id_Achats = models.ForeignKey(Achats, blank=True, on_delete=models.CASCADE)
   Id_Article = models.ForeignKey(Article, blank=True, on_delete=models.CASCADE)
   Prix_Unitaire = models.DecimalField(max_digits=10,decimal_places=2,default=0)
   Quantite = models.IntegerField(default=1)

   def __str__(self):
      return str(self.Id_Article)
