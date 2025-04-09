from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.formUser, name='formUser'),
    path('encuesta/<str:survey_type>/', views.survey_view, name='survey_view'),
    path('seleccionar-encuesta/', views.select_survey, name='select_survey'),
    path('anonimo/', views.aninomo, name='view_anonimo'),
    path('procesar-anonimo/', views.procesar_anonimo, name='procesar_anonimo'),
    path('seleccionar-tipo-experiencia/', views.seleccionar_tipo_experiencia, name='seleccionar_tipo_experiencia'),
    path('guardar_tipo/', views.guardar_tipo_experiencia, name='guardar_tipo_experiencia'),

]
