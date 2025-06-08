from django.contrib import admin
from .models import Estudiante, Survey, Question, Answer

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'ci', 'cycle', 'itinerary', 'email')
    search_fields = ('first_name', 'last_name', 'ci', 'email')
    list_filter = ('cycle', 'itinerary', 'tipo_experiencia')

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0  # No mostrar formularios extra vacíos
    readonly_fields = ('question', 'response') # Para que no se puedan editar desde aquí

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey_type', 'completed', 'created_at')
    list_filter = ('survey_type', 'completed')
    inlines = [AnswerInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'survey_type', 'section', 'question_type', 'order')
    list_filter = ('category', 'survey_type', 'section', 'question_type')
    ordering = ('category', 'survey_type', 'section', 'order')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('survey', 'question', 'response')