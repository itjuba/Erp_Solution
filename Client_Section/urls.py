
from django.contrib import admin
from django.urls import path,include
from .views import home,client,create_client
from django.conf import settings
from  django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home'),
    path('tables/',client,name='tables'),
    path('create/',create_client,name='create'),

]
