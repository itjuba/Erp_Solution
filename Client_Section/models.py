from django.db import models
from datetime import datetime

from .utils import unique_slug_generator
from django.db.models.signals import  pre_save

# Create your models here.




class Client_Data(models.Model):
     RC = models.CharField(max_length=50)
     Raison_social = models.CharField(max_length=254,blank=True)
     NIF = models.CharField(max_length=50,blank=True,unique=True)
     AI = models.CharField(max_length=50,blank=True,unique=True)
     NIS = models.CharField(max_length=50,blank=True,unique=True)
     Banque = models.CharField(max_length=50,blank=True,unique=True)
     CB = models.CharField(max_length=50)
     adresse = models.CharField(max_length=50)
     slug = models.SlugField(blank=True, unique=True)
     active = models.BooleanField(default=True)


     def __str__(self):
          return self.Name


def product_presave_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(product_presave_receiver,sender=Client_Data)