from django.urls import path
from .views import home,  formUser
from django.shortcuts import render


urlpatterns = [
    #path('',homeView, name='home'),
    path('', home, name='home'), 
    path('User', formUser, name='formUser'),

]

