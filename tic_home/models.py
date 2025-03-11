from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# Validador para asegurarse que solo se ingresen números del 1 al 9 en el ciclo
cycle_validator = RegexValidator(r'^[1-9]$', 'Ingrese un número entre 1 y 9.')

# Validador para asegurarse que solo se ingresen números en el campo 'ci'
ci_validator = RegexValidator(r'^\d{10}$', 'La cédula de identidad debe contener exactamente 10 números.')

# Validador para asegurarse que solo se ingresen letras en 'first_name' y 'last_name'
name_validator = RegexValidator(r"^[A-Za-záéíóúÁÉÍÓÚÑñ' -]+$", "El nombre debe contener solo letras, apóstrofes o guiones.")


# Validador para asegurarse que solo se ingresen letras en 'itinerary'
itinerary_validator = RegexValidator(r'^[A-Za-záéíóúÁÉÍÓÚÑñ ]+$', 'El itinerario debe contener solo letras.')

class User(models.Model):
    ci = models.CharField(max_length=10, unique=True, validators=[ci_validator])  
    first_name = models.CharField(max_length=50, validators=[name_validator]) 
    last_name = models.CharField(max_length=50, validators=[name_validator])  
    cycle = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])  # Evita valores fuera de rango 
    itinerary = models.CharField(max_length=50, validators=[itinerary_validator])  
    email = models.EmailField(unique=True, validators=[EmailValidator()])  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_completed_surveys(self):
        """Verifica si el usuario ha completado ambas encuestas."""
        return self.survey_set.filter(completed=True).values_list('survey_type', flat=True).count() == 2


    # Sobrescribimos el método save para realizar la validación manualmente
    def save(self, *args, **kwargs):
        # Validamos todos los campos
        self.full_clean()
        super(User, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Survey(models.Model):
    TYPE_CHOICES = [
        ('pre', 'Encuesta I (Antes de la experiencia)'),
        ('post', 'Encuesta II (Después de la experiencia)'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con usuario
    survey_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.survey_type} - {self.user.first_name}"


class Question(models.Model):
    survey_type = models.CharField(max_length=10, choices=Survey.TYPE_CHOICES)  # Se vincula a un tipo de encuesta
    text = models.TextField()

    def __str__(self):
        return self.text

    
class Answer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)  # Relación con la encuesta
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Relación con la pregunta
    response = models.TextField()

    def __str__(self):
        return f"Resp: {self.response} ({self.survey.survey_type} - {self.survey.user.first_name})"

