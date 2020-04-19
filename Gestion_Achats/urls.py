
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from .views import find, Article_table,view,article_create,Achats_delete,Article_update,Article_delete,Achats_table,Achats_create,Achats_update



urlpatterns = [
    path('view/',view,name='view'),
    path('find',find,name='find'),
    path('article/',Article_table,name='article'),
    path('article_create/',article_create,name='article_create'),
    path('article_update/<int:pk>',Article_update,name='article_update'),
    path('article_delete/<int:pk>',Article_delete,name='article_delete'),

    path('achats/', Achats_table, name='achats'),
    path('achats_create/', Achats_create, name='achats_create'),
    path('achats_update/<int:pk>',Achats_update,name='achats_update'),
    path('achats_delete/<int:pk>', Achats_delete, name='achats_delete'),



]
