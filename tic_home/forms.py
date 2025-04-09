from django import forms
from .models import Estudiante, Answer

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['first_name', 'last_name', 'ci', 'cycle', 'itinerary', 'email', 'tipo_experiencia']
        widgets = {
            'cycle': forms.Select(choices=Estudiante.CYCLE_CHOICES),
            'itinerary': forms.Select(choices=Estudiante.ITINERARY_CHOICES),
            'tipo_experiencia': forms.Select(choices=Estudiante.TIPO_EXPERIENCIA_CHOICES),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'ci': 'Cédula de Identidad',
            'cycle': 'Ciclo',
            'itinerary': 'Itinerario',
            'email': 'Correo Electrónico',
            'tipo_experiencia': 'Tipo de experiencia'
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