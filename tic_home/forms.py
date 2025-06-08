from django import forms
from .models import Estudiante, Answer

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['tipo_experiencia']
        widgets = {
            'ci': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-3 bg-slate-100 border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: 1234567890'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-3 bg-slate-100 border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-4 py-3 bg-slate-100 border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Tu apellido'
            }),
            'cycle': forms.Select(attrs={
                'class': 'mt-1 block w-full px-4 py-3 bg-slate-100 border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
            }),
            'itinerary': forms.Select(attrs={
                'class': 'mt-1 block w-full px-4 py-3 bg-slate-100 border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full px-4 py-3 bg-slate-100 border-slate-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'tu.correo@ejemplo.com'
            }),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'ci': 'Cédula de Identidad',
            'cycle': 'Ciclo',
            'itinerary': 'Itinerario',
            'email': 'Correo Electrónico',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
        labels = {
            'response': 'Respuesta',
        }