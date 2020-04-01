from django.db import models
from datetime import datetime

from .utils import unique_slug_generator
from django.db.models.signals import  pre_save

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


def product_presave_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(product_presave_receiver,sender=Client_Data)