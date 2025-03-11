from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Importar el modelo de usuario

def register_user(request):
    if request.method == 'GET':
        print('enviando fomr')
    else:
        print(request.POST)
        print('obteniendo datos')

    return render(request, "home/register.html")
