
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from  django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.Transaction_View,name='transaction_view'),
    path('trans_delete/<int:pk>',views.trans_delete,name='trans_delete'),
    path('trans_update/<int:pk>',views.trans_update,name='trans_update'),
    path('trans_create',views.trans_create,name='trans_create'),

]
