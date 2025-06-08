from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

# Validadores (mantén los que ya tienes)
cycle_validator = RegexValidator(r'^[1-9]$', 'Ingrese un número entre 1 y 9.')
ci_validator = RegexValidator(r'^\d{10}$', 'La cédula de identidad debe contener exactamente 10 números.')
name_validator = RegexValidator(r"^[A-Za-záéíóúÁÉÍÓÚÑñ' -]+$", "El nombre debe contener solo letras, apóstrofes o guiones.")
itinerary_validator = RegexValidator(r'^[A-Za-záéíóúÁÉÍÓÚÑñ ]+$', 'El itinerario debe contener solo letras.')

class Estudiante(models.Model):  # Cambié el nombre de User a Estudiante para evitar conflictos
    ITINERARY_CHOICES = [
        ('software', 'Ingeniería de Software'),
        ('inteligentes', 'Sistemas Inteligentes'),
        ('aplicada', 'Computación Aplicada'),
    ]
    CYCLE_CHOICES = [(str(i), str(i)) for i in range(1, 10)]

    TIPO_EXPERIENCIA_CHOICES = [
        ('inmersiva', 'Realidad Virtual Inmersiva'),
        ('no_inmersiva', 'Realidad Virtual No Inmersiva'),
    ]

    ci = models.CharField(max_length=10, unique=True, validators=[ci_validator])  
    first_name = models.CharField(max_length=50, validators=[name_validator]) 
    last_name = models.CharField(max_length=50, validators=[name_validator])  
    cycle = models.CharField(max_length=2, choices=CYCLE_CHOICES)
    itinerary = models.CharField(max_length=20, choices=ITINERARY_CHOICES)
    email = models.EmailField(unique=True, validators=[EmailValidator()])  
    tipo_experiencia = models.CharField(max_length=20, choices=TIPO_EXPERIENCIA_CHOICES, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_anonymous(self):
        return self.first_name.startswith('Anonimo')

    def has_completed_surveys(self):
        """Verifica si el usuario ha completado ambas encuestas."""
        completed_surveys = self.survey_set.filter(completed=True).values_list('survey_type', flat=True)
        return set(completed_surveys) == {'pre', 'post'}

    def save(self, *args, **kwargs):
        """Sobreescribir save para validar antes de guardar."""
        self.full_clean()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

class Survey(models.Model):
    TYPE_CHOICES = [
        ('pre', 'Encuesta I (Antes de la experiencia)'),
        ('post', 'Encuesta II (Después de la experiencia)'),
    ]
    
    user = models.ForeignKey(Estudiante, on_delete=models.CASCADE)  # Cambiado a Estudiante
    survey_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Agregado para ordenación

    def __str__(self):
        return f"{self.get_survey_type_display()} - {self.user.first_name}"

class Question(models.Model):
    SECTION_CHOICES = [
        ('utilidad', 'Utilidad Percibida'),
        ('facilidad', 'Facilidad de Uso Percibida'),
        ('actitud', 'Actitud hacia el Uso'),
        ('intencion', 'Intención de Uso'),
    ]

    QUESTION_TYPE_CHOICES = [
        ('cerrada', 'Cerrada'),
        ('abierta', 'Abierta'),
    ]

    survey_type = models.CharField(max_length=10, choices=Survey.TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=Estudiante.TIPO_EXPERIENCIA_CHOICES, default='inmersiva')
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='utilidad')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='cerrada')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'survey_type', 'section', 'order']

    def __str__(self):
        return f"({self.get_category_display()}/{self.get_survey_type_display()}) - {self.text}"

class Answer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="answers")  
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")  
    response = models.TextField()

    def __str__(self):
        return f"Resp: {self.response} ({self.survey.get_survey_type_display()} - {self.survey.user.first_name})"
    
