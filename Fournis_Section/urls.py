
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from .views import home,client, client_create,client_update,client_delete,see,contact_Fournis,F_create_contact,\
    contact_update_fournis,contact_delete




urlpatterns = [
    path('',home,name='home'),
    path('fournis/',client,name='fournis'),
    path('Fournis_contact/',contact_Fournis,name='Fournis_contact'),
    path('Fournis_create/',client_create,name='Fournis_create'),
    path('F_create_contact/',F_create_contact,name='F_create_contact'),
    path('Fournis_update/<slug:slug>',client_update, name='Fournis_update'),
    path('Fournus_update_contact/<int:pk>/',contact_update_fournis, name='Fournus_update_contact'),
    path('Fournis_delete/<slug:slug>',client_delete, name='Fournis_delete'),
    path('Fournis_contact_delete/<int:pk>',contact_delete, name='Fournis_contact_delete'),
    path('Fournis_see/<slug:slug>',see, name='Fournis_see'),

]
