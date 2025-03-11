from django.shortcuts import render, redirect
from .forms import UserForm
""" from django.http import HttpResponse
from django.contrib import messages
from .models import User, Survey   # Importar el modelo de usuario """


def home(request):
    return render(request, "home/home.html")

def formUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario en la base de datos
            return redirect('home')  # Redirige a la página de inicio o donde desees
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, "home/formUser.html", {'form': form})

""" def register_user(request):
    if request.method == 'GET':
        print('enviando fomr')
    else:
        print(request.POST)
        print('obteniendo datos')

    return render(request, "home/register.html")

def survey(request):
    return render(request, "home/survey.html") """
