from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'ci', 'cycle', 'itinerary', 'email']
        widgets = {
            'cycle': forms.Select(choices=User.CYCLE_CHOICES),
            'itinerary': forms.Select(choices=User.ITINERARY_CHOICES),
        }
