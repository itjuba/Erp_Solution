
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.caisse_view,name='caisse'),
    path('caisse_create',views.caisse_create,name='caisse_create'),
    path('caisse_update/<int:pk>',views.caisse_update,name='caisse_update'),
    path('caisse_delete/<int:pk>',views.caisse_delete,name='caisse_delete'),
    path('alim_caisse/',views.alim_caisse,name='alim_caisse'),

]
