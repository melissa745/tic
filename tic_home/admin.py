from django.contrib import admin
from .models import Estudiante, Survey, Question, Answer

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'ci', 'cycle', 'itinerary', 'email')
    search_fields = ('first_name', 'last_name', 'ci', 'email')

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey_type', 'completed')
    list_filter = ('survey_type', 'completed')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey_type', 'order')
    list_filter = ('survey_type',)
    # Elimina cualquier método get_survey_type que estés intentando usar
    # Ya no es necesario porque survey_type es un campo directo ahora

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'response')