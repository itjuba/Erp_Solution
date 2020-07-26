
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from . import views

urlpatterns = [
    path('view/',views.Chareg_view,name='charge_view'),
    path('create_charge/',views.charge_create,name='create_charge'),
    path('charge_update/<int:pk>/',views.charge_update,name='charge_update'),
    path('charge_delete/<int:pk>/',views.charge_delete,name='charge_delete'),
    path('charge_pay/<int:pk>/',views.payement_charge_create,name='charge_pay'),
]
