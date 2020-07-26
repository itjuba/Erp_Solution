from django.db import models

# Create your models here.



class Charge(models.Model):
    class Designation(models.TextChoices):
        Casnos = "Casnos"
        Cnas = "Cnas"
        Salaire = "Salaire"
        G50 = "G50"
        Bilan = "Bilan"
        Notaire = 'Notaire'
        Charge_diver = 'Charge diver'

    Date = models.DateField()
    Date_limit = models.DateField()
    Etat = models.BooleanField(default=False)
    Montant = models.DecimalField(max_digits=10,decimal_places=2)
    Description = models.TextField()
    Designation_charge = models.CharField(choices=Designation.choices,max_length=200)


    def __str__(self):
        return self.Description