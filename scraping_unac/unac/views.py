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
    ids_alumnos_base_datos = [2, 3, 133, 6, 8, 137, 138, 12, 15, 16, 17, 131, 150,
                              23, 153, 27, 29, 30, 32, 161, 34, 36, 134, 38, 41,
                              42, 171, 173, 48, 52, 53, 59, 61, 63, 64, 68, 69,
                              77, 86, 87, 164, 98, 166, 104, 107, 108, 115, 116,
                              169, 125]
    notas_alumnos = Notas.objects.filter(alumno_id__in=ids_alumnos_base_datos)
    result_final = {}
    for nota in notas_alumnos:
        if '(E)' not in nota.curso.nombre:
            if nota.alumno_id in result_final.keys():
                result_final[nota.alumno_id][nota.curso.nombre] = nota.nota
            else:
                result_final[nota.alumno_id] = {}
                result_final[nota.alumno_id]['CODIGO ALUMNO'] = nota.alumno.codigo
                result_final[nota.alumno_id][nota.curso.nombre] = nota.nota

    print ('results', result_final)
    print ('alumnos keuys', result_final.keys())
    print ('alumnos keuys', len(result_final.keys()))

    ## Creo todas las cabeceras de mi csv
    cabeceras = set()
    for key in result_final.keys():
        cabeceras.update(result_final[key].keys())
    ## Genero el CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_format_1.csv"'
    writer = csv.DictWriter(response, cabeceras)
    writer.writeheader()
    for k in result_final:
        # writer.writerow()
        writer.writerow({field: result_final[k].get(field) for field in cabeceras})

    return response



