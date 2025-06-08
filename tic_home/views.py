from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Estudiante, Survey, Question, Answer
from .forms import EstudianteForm, AnswerForm
import random
from django.core.validators import EmailValidator
from django.template.loader import render_to_string
from weasyprint import HTML

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

            # Redirigir a la selección de tipo de experiencia
            return redirect('seleccionar_tipo_experiencia')
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

    # Obtener el tipo de experiencia del estudiante
    experience_type = estudiante.tipo_experiencia
    if not experience_type:
        messages.error(request, "Debe seleccionar un tipo de experiencia antes de continuar.")
        return redirect('seleccionar_tipo_experiencia')

    # Obtener o crear la encuesta correspondiente
    survey, created = Survey.objects.get_or_create(
        survey_type=survey_type, 
        user=estudiante
    )

    # Obtener las preguntas para este tipo de encuesta y categoría
    questions = Question.objects.filter(
        survey_type=survey_type,
        category=experience_type
    )
    
    # Si no hay preguntas, redirigir con un mensaje
    if not questions.exists():
        messages.error(request, f"No hay preguntas disponibles para la encuesta '{survey.get_survey_type_display()}' en la categoría seleccionada.")
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
                return redirect('select_survey')
            else:  # post
                messages.success(request, "¡Ha completado todas las encuestas! Gracias por su participación.")
                return redirect('view_results')
        else:
            messages.error(request, "Por favor, responda al menos una pregunta antes de enviar la encuesta.")

    # Obtener respuestas existentes (si las hay)
    existing_answers = {}
    for answer in Answer.objects.filter(survey=survey):
        existing_answers[answer.question_id] = answer.response
        
    # Agrupar preguntas por sección para la plantilla
    sections = {}
    for question in questions:
        section_name = question.get_section_display()
        if section_name not in sections:
            sections[section_name] = []
        sections[section_name].append(question)

    return render(request, 'home/survey_form.html', {
        'survey': survey,
        'sections': sections,
        'survey_type': survey_type,
        'existing_answers': existing_answers,
        'estudiante': estudiante
    })

def view_results(request):
    estudiante_id = request.session.get('estudiante_id')
    if not estudiante_id:
        messages.error(request, "No se ha encontrado un participante. Por favor, inicie sesión de nuevo.")
        return redirect('home')

    try:
        estudiante = Estudiante.objects.get(id=estudiante_id)
    except Estudiante.DoesNotExist:
        messages.error(request, "Estudiante no encontrado.")
        return redirect('home')

    # Diccionario para almacenar los datos de los gráficos
    results_data = {
        'pre': {},
        'post': {}
    }
    
    # Obtener todas las secciones de las preguntas
    sections = Question.SECTION_CHOICES

    for survey_type in ['pre', 'post']:
        survey = Survey.objects.filter(user=estudiante, survey_type=survey_type).first()
        if not survey:
            continue

        for section_key, section_name in sections:
            # Obtener todas las respuestas para las preguntas cerradas de esta sección
            answers_qs = Answer.objects.filter(
                survey=survey,
                question__category=estudiante.tipo_experiencia,
                question__section=section_key,
                question__question_type='cerrada'
            ).values_list('response', flat=True)
            
            # Convertir a lista para poder usar el método .count() de las listas
            answers_list = list(answers_qs)

            # Contar la frecuencia de cada respuesta (1-5)
            # 1, 2 = Negativa; 3 = Neutral; 4, 5 = Positiva
            negative_count = answers_list.count('1') + answers_list.count('2')
            neutral_count = answers_list.count('3')
            positive_count = answers_list.count('4') + answers_list.count('5')
            
            counts = [negative_count, neutral_count, positive_count]
            
            results_data[survey_type][section_name] = counts

    return render(request, 'home/results.html', {
        'estudiante': estudiante,
        'results_data': results_data
    })

def generate_pdf_report(request):
    estudiante_id = request.session.get('estudiante_id')
    if not estudiante_id:
        return HttpResponse("No autorizado.", status=403)

    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    
    report_data = {'pre': {}, 'post': {}}
    
    questions = Question.objects.filter(category=estudiante.tipo_experiencia).order_by('section', 'order')

    for survey_type in ['pre', 'post']:
        survey = Survey.objects.filter(user=estudiante, survey_type=survey_type).first()
        if survey:
            # Agrupar preguntas por sección
            sections_data = {}
            for question in questions.filter(survey_type=survey_type):
                section_name = question.get_section_display()
                if section_name not in sections_data:
                    sections_data[section_name] = []
                
                answer = Answer.objects.filter(survey=survey, question=question).first()
                sections_data[section_name].append({
                    'question': question.text,
                    'answer': answer.response if answer else "Sin respuesta"
                })
            report_data[survey_type] = sections_data

    # Renderizar la plantilla HTML
    html_string = render_to_string('home/report.html', {
        'estudiante': estudiante,
        'report_data': report_data
    })
    
    # Crear el PDF
    pdf = HTML(string=html_string).write_pdf()

    # Devolver la respuesta como PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{estudiante.ci}.pdf"'
    
    return response

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


# ENCUESTA PARA VERIFICAR SI EL USUARIO ES ANINIMO O NO

def aninomo(request):
    return render (request, 'home/anonimo.html')

def procesar_anonimo(request):
    if request.method == 'POST':
        opcion = request.POST.get('anonimo')
        if opcion == 'si':
            request.session['anonimo'] = True
            
            count = Estudiante.objects.filter(first_name__startswith="Anonimo").count() + 1

            # Generar campos válidos
            ci = f"{random.randint(1000000000, 9999999999)}"  # 10 dígitos
            first_name = f"Anonimo"  # sin números, válido
            last_name = f"Anonimo"  # como está validado, lo mejor es dejarlo en texto válido
            email = f"anonimo{count}@anonimo.com"

            estudiante = Estudiante.objects.create(
                ci=ci,
                first_name=first_name,
                last_name=last_name,
                cycle=str(random.randint(1, 9)),  # entre '1' y '9'
                itinerary='software',  # opción válida de ITINERARY_CHOICES
                email=email,
            )

            request.session['estudiante_id'] = estudiante.id

            # Crear encuesta tipo "pre"
            Survey.objects.create(user=estudiante, survey_type='pre')

            return redirect('seleccionar_tipo_experiencia')
        else:
            request.session['anonimo'] = False
            return redirect('formUser')
        
# SELECCIONAR TIPO DE EXPERIENCIA 
def seleccionar_tipo_experiencia(request):
    return render(request, 'home/seleccionar_tipo.html', {'choices': Estudiante.TIPO_EXPERIENCIA_CHOICES})

def guardar_tipo_experiencia(request):
    if request.method == 'POST':
        tipo = request.POST.get("tipo")
        estudiante_id = request.session.get('estudiante_id')

        if not estudiante_id:
            messages.error(request, "No se encontró un estudiante en la sesión. Por favor, regístrese de nuevo.")
            return redirect('home')

        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            estudiante.tipo_experiencia = tipo
            estudiante.save()
            request.session["tipo_experiencia"] = tipo

            # Redirigir a la encuesta 'pre'
            return redirect('survey_view', survey_type='pre')
        except Estudiante.DoesNotExist:
            messages.error(request, "Estudiante no encontrado. Por favor, regístrese de nuevo.")
            return redirect('home')


