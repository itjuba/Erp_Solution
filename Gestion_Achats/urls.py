
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from .views import find,payement,step1,update_payement,payement_create,update,achat_view_update,step2,ContactWizard,Achats_create2 ,Article_table,view,article_create,Achats_delete,Article_update,Article_delete,Achats_table,Achats_create,Achats_update
from .forms import AchatForm,AssociationForm


urlpatterns = [
    path('view/',view,name='view'),
    path('find',find,name='find'),
    path('article/',Article_table,name='article'),
    path('article_create/',article_create,name='article_create'),
    path('article_update/<int:pk>',Article_update,name='article_update'),
    path('article_delete/<int:pk>',Article_delete,name='article_delete'),

    path('achats/', Achats_table, name='achats'),
    path('show/', view, name='show'),
    path('achats_create/', Achats_create, name='achats_create'),
    path('achats_create2/', Achats_create2, name='achats_create2'),
    path('achats_update/<int:pk>',Achats_update,name='achats_update'),
    path('achats_update_view/<int:pk>',achat_view_update,name='achats_update_view'),

    path('achats_delete/<int:pk>', Achats_delete, name='achats_delete'),
    path('step1/', step1, name='step1'),
    path('step2/', step2, name='step2'),
    path('update_achat/<int:pk>', update, name='update_achat'),


    path('payement_create/<int:pk>', payement_create, name='payement_create'),
    path('payement_update/<int:pk>', update_payement, name='payement_update'),
    path('payements/', payement, name='payements'),














]
