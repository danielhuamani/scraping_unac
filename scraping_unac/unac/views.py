from django.shortcuts import render
from django.http import JsonResponse
from .scraping_cursos import Scraping
from .models import Curso


def cursos(request):
    codigo = request.GET.get('codigo')
    if codigo:
        curso = Scraping(codigo)
        alumno = curso.save_alumno()
    cursos = Curso.objects.values_list('codigo', 'nombre', 'electivo', 'credito')
    data = {
        'alumno': alumno.alumno
    }
    return JsonResponse(data, safe=False)
