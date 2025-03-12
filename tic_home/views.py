from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Estudiante, Survey, Question, Answer
from .forms import EstudianteForm, AnswerForm

def home(request):
    return render(request, "home/home.html")

def formUser(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()  # Guarda el nuevo estudiante
            request.session['estudiante_id'] = estudiante.id  # Guarda el ID en la sesión
            
            # Crear la encuesta 'pre' asociada al estudiante
            survey = Survey.objects.create(user=estudiante, survey_type='pre')

            # Redirigir a la encuesta 'pre'
            return redirect('survey_view', survey_type='pre')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = EstudianteForm()
    
    return render(request, "home/formUser.html", {'form': form})

def survey_view(request, survey_type):
    # Recuperar el estudiante_id de la sesión
    estudiante_id = request.session.get('estudiante_id')

    # Verificar que el estudiante_id esté en la sesión
    if not estudiante_id:
        messages.error(request, "Debe registrarse primero para acceder a las encuestas.")
        return redirect('home')  # Redirige a la página principal

    # Obtener el estudiante usando el ID almacenado en la sesión
    try:
        estudiante = Estudiante.objects.get(id=estudiante_id)
    except Estudiante.DoesNotExist:
        messages.error(request, "Estudiante no encontrado. Por favor, regístrese nuevamente.")
        return redirect('home')

    # Obtener o crear la encuesta correspondiente para ese estudiante y tipo
    survey, created = Survey.objects.get_or_create(
        survey_type=survey_type, 
        user=estudiante
    )

    # Obtener las preguntas para este tipo de encuesta
    questions = Question.objects.filter(survey_type=survey_type)
    
    # Si no hay preguntas, redirigir con un mensaje
    if not questions.exists():
        messages.error(request, f"No hay preguntas disponibles para la encuesta {survey.get_survey_type_display()}.")
        return redirect('home')

    if request.method == 'POST':
        # Verificar si hay respuestas enviadas
        has_responses = False
        
        # Guardar respuestas del estudiante
        for question in questions:
            response = request.POST.get(f'question_{question.id}')
            if response:
                has_responses = True
                # Verificar si la respuesta ya existe y actualizarla, o crear nueva
                Answer.objects.update_or_create(
                    survey=survey,
                    question=question,
                    defaults={'response': response}
                )
        
        if has_responses:
            survey.completed = True
            survey.save()
            
            # Si completó la encuesta pre, crear la encuesta post
            if survey_type == 'pre':
                Survey.objects.get_or_create(user=estudiante, survey_type='post')
                messages.success(request, "Encuesta completada con éxito. Ahora puede realizar la segunda encuesta cuando esté listo.")
                return redirect('survey_view', survey_type='post') # O redirigir a una página intermedia
            else:  # post
                messages.success(request, "¡Ha completado todas las encuestas! Gracias por su participación.")
                return redirect('home')
        else:
            messages.error(request, "Por favor, responda al menos una pregunta antes de enviar la encuesta.")

    # Obtener respuestas existentes (si las hay)
    existing_answers = {}
    for answer in Answer.objects.filter(survey=survey):
        existing_answers[answer.question_id] = answer.response

    return render(request, 'home/survey_form.html', {
        'survey': survey,
        'questions': questions,
        'survey_type': survey_type,
        'existing_answers': existing_answers,
        'estudiante': estudiante
    })

# Agregar una nueva vista para seleccionar encuesta (útil para acceder a la encuesta post)
def select_survey(request):
    estudiante_id = request.session.get('estudiante_id')
    
    if not estudiante_id:
        messages.error(request, "Debe registrarse primero para acceder a las encuestas.")
        return redirect('home')
    
    try:
        estudiante = Estudiante.objects.get(id=estudiante_id)
        surveys = Survey.objects.filter(user=estudiante)
        
        return render(request, 'home/select_survey.html', {
            'surveys': surveys,
            'estudiante': estudiante
        })
    except Estudiante.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
        return redirect('home')
