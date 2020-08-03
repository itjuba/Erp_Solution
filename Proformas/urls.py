from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from Proformas import views
urlpatterns = [
    path('',views.Commande_view,name="commande"),
    path('search',views.ajax_live,name="search"),
    path('facture',views.facture_view,name="facture"),

    path('step1',views.step1,name="step1"),
    path('step2',views.step2,name="step2"),
    path('step3',views.step3,name="step3"),

    path('send/<int:pk>',views.send_mail,name="send"),

    path('valid/<int:pk>',views.dat_val,name="valid"),

    path('delete_commande/<int:pk>',views.commande_deletee,name="delete_commande"),

    path('delete_facture/<int:pk>',views.facture_delete,name="delete_facture"),
    path('update_facture/<int:pk>',views.facture_update,name="facture_update"),
    path('create_facture/<int:pk>',views.Facture_create,name="create_facture"),
    path('create_payements_f/<int:pk>',views.payement_c,name="create_payements_f"),
    path('pdf/<int:pk>',views.html_to_pdf_view,name="pdf"),
    
    path('update2/<int:pk>',views.update2,name="update2"),
    path('update1/<int:pk>',views.update1,name="update1"),
    path('update2post/<int:pk>',views.update2post,name="update2post"),
    




    path('commande_update/<int:pk>',views.commande_update,name="update_commande"),


    path('pdf_facture/<int:pk>',views.html_to_pdf_view_facture,name="pdf_facture"),
    path('update_com_d/<int:pk>',views.update_com_d,name="update_com_d"),
    path('test',views.test,name='test'),
    path('test2',views.test2,name='test2'),



]
