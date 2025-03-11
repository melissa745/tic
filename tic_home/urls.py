from django.urls import path
from .views import register_user 
from django.shortcuts import render


urlpatterns = [
    #path('',homeView, name='home'),
    path('', register_user, name='register'),  # Cambia 'homeView' si no existe

]

