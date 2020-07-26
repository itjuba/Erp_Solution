
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from .views import home,client,\
 client_create,client_update,client_delete,see,contact,Contact_create,\
    contact_update,contact_delete,graph,ajax,ajax_pay,ajax_trans




urlpatterns = [
    path('',home,name='home'),
    path('graph',graph,name='graph'),
    path('ajax',ajax,name='ajax'),
    path('ajax2',ajax_pay,name='ajax2'),
    path('ajax_trans',ajax_trans,name='ajax_trans'),


    path('client/',client,name='client'),
    path('contact/',contact,name='contact'),
    path('create/',client_create,name='create'),
    path('create_contact/',Contact_create,name='create_contact'),
    path('update/<slug:slug>',client_update, name='update'),
    path('update_contact/<int:pk>/',contact_update, name='contact_update'),
    path('delete/<slug:slug>',client_delete, name='delete'),
    path('contact_delete/<int:pk>',contact_delete, name='contact_delete'),
    path('see/<slug:slug>',see, name='see'),

]
