from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
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
