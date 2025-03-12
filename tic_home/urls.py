from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.formUser, name='formUser'),
    path('encuesta/<str:survey_type>/', views.survey_view, name='survey_view'),
    path('seleccionar-encuesta/', views.select_survey, name='select_survey'),
]
