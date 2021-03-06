"""Stage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based viewsachat_article
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from Client_Section.views import graph
from  django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/',include('Client_Section.urls')),
    path('fournis/',include('Fournis_Section.urls')),
    path('achat_article/',include('Gestion_Achats.urls')),
    path('commande/',include('Proformas.urls')),
    path('charge/',include('Charge.urls')),
    path('transaction/',include('Transactionb.urls')),
    path('Caisse/',include('Caisse.urls')),
    path('account/',include('Accounts.urls')),
    path('home/',graph,name="homme"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
