
from django.contrib import admin
from django.urls import path,include
from .views import home,client,client_create,client_update,client_delete,see
from django.conf import settings
from  django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home'),
    path('tables/',client,name='tables'),
    path('create/',client_create,name='create'),
    path('update/<slug:slug>',client_update, name='update'),
    path('delete/<slug:slug>',client_delete, name='delete'),
    path('see/<slug:slug>',see, name='see'),

]
