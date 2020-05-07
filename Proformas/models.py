from django.db import models

# Create your models here.

from Client_Section.models import Client_Data


class Commande(models.Model):
    class Service(models.TextChoices):
        Hébergmeent = "Hébergmeent"
        Assistance = "Assistance"
        Réseau = "Réseau"
        Développement = "Développement"
        Matérial = "Matérial"

    Date = models.DateField()
    Date_validation = models.DateField(null=True,blank=True)
    Client = models.ForeignKey(Client_Data, on_delete=models.CASCADE)
    Numero_commande = models.CharField(max_length=200)
    Montant_HT = models.DecimalField(max_digits=10, decimal_places=2)
    Montant_TVA = models.DecimalField(max_digits=10, decimal_places=2)
    Montant_TTC = models.DecimalField(max_digits=10, decimal_places=2)
    Type_Service = models.CharField(choices=Service.choices, max_length=200)
    validation = models.BooleanField(default=False)

    def __str__(self):
        return self.Numero_commande


class Modalite(models.Model):

    modalite_payement = models.TextField(blank=True,null=True,default='')
    Arret_Facture = models.TextField(blank=True,null=True,default='')
    Formation = models.TextField(blank=True,null=True,default='')
    Period_Réalisation = models.TextField(blank=True,null=True,default='')
    Echéancier_payement = models.TextField(blank=True,null=True,default='')
    Debut_realsiation = models.TextField(blank=True,null=True,default='')
    Command = models.ForeignKey(Commande, on_delete=models.CASCADE, default='')
    Garantie = models.TextField(blank=True,null=True,default='')


    def __str__(self):
        return self.modalite_payement




class Commande_Designation(models.Model):
    Designation = models.TextField()
    Prix_Unitaire = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Command = models.ForeignKey(Commande,on_delete=models.CASCADE)
    Quantite = models.IntegerField(default=1)
    Montant_HT = models.DecimalField(max_digits=10, decimal_places=2)
    Montant_TVA = models.DecimalField(max_digits=10, decimal_places=2)
    Montant_TTC = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.Designation
