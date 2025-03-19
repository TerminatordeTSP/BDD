"""
URL configuration for BddINT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from bddint_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('requettes/', views.requettes, name='requettes'),
    path('localisation/', views.localisation, name='localisation'),
    path('camions/', views.camions, name='camions'),
    path('chauffeurs/', views.chauffeurs, name='chauffeurs'),
    path('camions_update/<str:id>/', views.camions_update, name='camions_update'),
    path('chauffeurs_update/<str:numéro_de_permis_de_conduire>/', views.chauffeurs_update, name='chauffeurs_update'),
    path('chauffeurs_delete/<str:numéro_de_permis_de_conduire>/', views.chauffeurs_delete, name='chauffeurs_delete'),
    path('camions_insert/', views.camions_insert, name='camions_insert'),
    path('vue_affectation_chauffeur/', views.vue_affectation_chauffeur, name='vue_affectation_chauffeur'),
    path('vue_logisticien/', views.vue_logisticien, name='vue_logisticien'),

]