from django.db import models
from Gestion_Achats.models import Payements
from django.db.models.signals import post_delete, post_save
from django.db.models import signals
# Create your models here.


class Transactionb(models.Model):
    Date = models.DateField()
    Date_transaction = models.DateField(null=True,blank=True)
    validation = models.CharField(max_length=200,null=True,blank=True)
    E_S = models.CharField(max_length=10)
    mode_de_payement = models.CharField( max_length=200,blank=True)
    reference = models.IntegerField(blank=True,null=True)
    Montant_HT = models.DecimalField(max_digits=10, decimal_places=2)
    Montant_TVA = models.DecimalField(max_digits=10, decimal_places=2)
    Montant_TTC = models.DecimalField(max_digits=10, decimal_places=2)
    Numero_facture = models.IntegerField(blank=True,null=True)
    Numero_payement = models.IntegerField()


    def __str__(self):
        return str(self.Date)

def create_t(sender, instance, created, *args, **kwargs):
  pay = instance
  if created:
    if instance.mode_de_payement =="Chéque" or instance.mode_de_payement == "virement bancaire":
        Transactionb.objects.bulk_create([
            Transactionb(Date=instance.Date,Numero_facture=instance.Numero_facture,Numero_payement=instance.Numero_payement,reference=instance.reference,Montant_HT=instance.Montant_HT,Montant_TVA=instance.Montant_TVA,Montant_TTC=instance.Montant_TTC,mode_de_payement=instance.mode_de_payement,E_S=instance.E_S)])

post_save.connect(create_t, sender=Payements)