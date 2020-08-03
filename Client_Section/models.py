from django.db import models
from datetime import datetime

from .utils import unique_slug_generator
from django.db.models.signals import  pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.




class Client_Data(models.Model):
     RC = models.CharField(max_length=50,unique=True,blank=True,null=True)
     Raison_social = models.CharField(max_length=254,unique=True)
     NIF = models.CharField(max_length=50,unique=True,blank=True,null=True)
     AI = models.CharField(max_length=50,unique=True,blank=True,null=True)
     NIS = models.CharField(max_length=50,unique=True,blank=True,null=True)
     Banque = models.CharField(max_length=50,blank=True,null=True)
     CB = models.CharField(max_length=50,unique=True,blank=True,null=True)
     adresse = models.CharField(max_length=150)
     slug = models.SlugField(blank=True, unique=True)
     active = models.BooleanField(default=True,blank=True,null=True)


     def __str__(self):
          return self.Raison_social


def product_presave_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(product_presave_receiver,sender=Client_Data)



class Contact(models.Model):
     client = models.ForeignKey(Client_Data,blank=True,on_delete=models.CASCADE)
     Nom = models.CharField(max_length=50)
     post = models.CharField(max_length=50,blank=True,null=True)
     Tel = models.CharField(max_length=50)
     email = models.EmailField(max_length=255,unique=True,blank=True,null=True)
     contact_type = models.CharField(default='Client_contact',max_length=50)


     def __str__(self):
          return self.post








