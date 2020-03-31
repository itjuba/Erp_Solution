from django.db import models
from datetime import datetime

# Create your models here.




class Client_Data(models.Model):
     Name = models.CharField(max_length=50)
     RC = models.CharField(max_length=50)
     tel = models.CharField(max_length=50)
     fax = models.CharField(max_length=50)
     adresse = models.CharField(max_length=50)
     slug = models.SlugField(blank=True, unique=True)
     active = models.BooleanField(default=True)


     def __str__(self):
          return self.Name
