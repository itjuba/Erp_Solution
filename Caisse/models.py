from django.db import models

# Create your models here.


class Caisse(models.Model):
    class ES(models.TextChoices):
        Vente = "Vente"
        Charge = "Charge"
        Dépence  = "Dépence"

    ES = models.CharField(choices=ES.choices, max_length=200)
    Date = models.DateField()
    Nature = models.TextField()
    Montant = models.DecimalField(max_digits=10, decimal_places=2)
