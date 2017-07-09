import csv
import itertools

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from .scraping_cursos import Scraping
from .models import Curso, Alumnos, Anio, Notas


def cargar_data(request):
    codigo = request.GET.get('codigo')
    if codigo:
        curso = Scraping(codigo)
        curso.get_data()
    alumnos = Alumnos.objects.values_list('alumno', 'codigo')
    cursos = Curso.objects.select_related('ciclo').values_list('nombre', 'codigo', 'electivo', 'ciclo')
    anios = Anio.objects.values_list('anio')
    notas = Notas.objects.select_related('alumno').values_list('alumno', 'curso', 'nota')
    data = {
        'alumnos': list(alumnos),
        'cursos': list(cursos),
        'anios': list(anios),
        'notas': list(notas)
    }
    return JsonResponse(data)


def index(request):
    return render(request, "index.html", locals())


def alumnos(request):
    alumnos = Alumnos.objects.all().order_by("-creado")
    if request.method == "POST":
        codigo = request.POST.get("codigo", False)
        if codigo:
            curso = Scraping(codigo)
            curso.get_data()
            return redirect(reverse("unac:alumnos"))
    return render(request, "alumnos.html", locals())


def notas(request, pk):
    alumno = get_object_or_404(Alumnos, pk=pk)
    print (alumno)
    notas = Notas.objects.filter(alumno=alumno).prefetch_related("curso")
    print (notas)
    return render(request, "notas.html", locals())


def generate_csv_data_format_1(request):
    cod_alumno_universo = '1115220329'
    alumno_universo = Alumnos.objects.get(codigo=cod_alumno_universo)
    # Obtengo los cursos de la curricula antigua
    cursos_curricula_antigua = set([nota.curso.nombre for nota in Notas.objects.filter(alumno=alumno_universo).order_by('creatdo') if '(E)' not in nota.curso.nombre])
    cantidad_cursos = len(cursos_curricula_antigua)
    print ('cantidad cursos', cantidad_cursos)
    # Alumnos que han culminado la universidad
    alumnos = [alumno for alumno in Alumnos.objects.all() if alumno.get_cantidad_notas_no_electivos >= cantidad_cursos]
    print ('cantidad alumnos', len(alumnos))
    alumnos_egresados = []  # En teoria egresados, puede ser q  llevo el curso, pero no lo aprobo.
    for alumno in alumnos:
        notas = alumno.alumnos_set.all()
        cursos = [nota.curso.nombre for nota in notas if '(E)' not in nota.curso.nombre]
        if all([curso if curso in cursos else False for curso in cursos_curricula_antigua]):
            alumnos_egresados.append(alumno.id)
    print ('alumnos egresados', len(alumnos_egresados))
    ###
    # Creamos la estructura de nuestro dataset
    # {'id_alumno': {'MATEMATICA':15, 'LP1':14, ...}}
    notas_alumnos = Notas.objects.filter(alumno_id__in=alumnos_egresados).order_by('creatdo')
    result_final = {}
    for nota in notas_alumnos:
        if '(E)' not in nota.curso.nombre:
            if nota.alumno_id in result_final.keys():
                if nota.curso.nombre not in result_final[nota.alumno_id].keys():
                    if nota.nota == 'NSP':
                        result_final[nota.alumno_id][nota.curso.nombre] = 0
                    else:
                        result_final[nota.alumno_id][nota.curso.nombre] = nota.nota
                # ASGINAMOS EL RENDIMIENTO ACADEMICO
                if len(result_final[nota.alumno_id].keys()) == cantidad_cursos + 1:
                    print ('PSE EL IF')
                    total_notas = 0
                    for key in result_final[nota.alumno_id].keys():
                        if key != 'CODIGO ALUMNO':
                            total_notas += int(result_final[nota.alumno_id][key])
                    promedio = float(total_notas) / 55
                    result_final[nota.alumno_id]['PROMEDIO'] = promedio
                    if promedio >= 13:
                        result_final[nota.alumno_id]['RENDIMIENTO'] = 'A'
                    elif 11 <= promedio < 13:
                        result_final[nota.alumno_id]['RENDIMIENTO'] = 'B'
                    else:
                        result_final[nota.alumno_id]['RENDIMIENTO'] = 'C'
            else:
                result_final[nota.alumno_id] = {}
                result_final[nota.alumno_id]['CODIGO ALUMNO'] = nota.alumno.codigo
                if nota.nota == 'NSP':
                    result_final[nota.alumno_id][nota.curso.nombre] = 0
                else:
                    result_final[nota.alumno_id][nota.curso.nombre] = nota.nota

    # # Creo todas las cabeceras de mi csv
    cabeceras = set(cursos_curricula_antigua)
    for key in result_final.keys():
        cabeceras.update(result_final[key].keys())
    # # Genero el CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_format_1.csv"'
    writer = csv.DictWriter(response, cabeceras)
    writer.writeheader()
    for k in result_final:
        writer.writerow({field: result_final[k].get(field) for field in cabeceras})
    return response



