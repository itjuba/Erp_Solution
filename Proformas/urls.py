from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from Proformas import views
urlpatterns = [
    path('',views.Commande_view,name="commande"),
    path('step1',views.step1,name="step1"),
    path('step2',views.step2,name="step2"),
    path('step3',views.step3,name="step3"),
    path('pdf/<int:pk>',views.html_to_pdf_view,name="pdf"),

]
