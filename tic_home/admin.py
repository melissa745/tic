from django.contrib import admin
from .models import User, Survey, Question, Answer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('ci', 'first_name', 'last_name', 'cycle', 'email')
    search_fields = ('ci', 'first_name', 'last_name', 'email')
    list_filter = ('cycle',)

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey_type', 'completed')
    list_filter = ('survey_type', 'completed')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey_type')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'question', 'response')
    
    def get_user(self, obj):
        return obj.survey.user
    get_user.short_description = 'User'
