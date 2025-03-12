from django import forms
from .models import Estudiante, Answer

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['first_name', 'last_name', 'ci', 'cycle', 'itinerary', 'email']
        widgets = {
            'cycle': forms.Select(choices=Estudiante.CYCLE_CHOICES),
            'itinerary': forms.Select(choices=Estudiante.ITINERARY_CHOICES),
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