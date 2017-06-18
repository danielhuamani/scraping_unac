from django.shortcuts import render
from django.http import JsonResponse
from .scraping_cursos import CursoScraping
from .models import Curso


def cursos(request):
    data = {}
    codigo = request.GET.get('codigo')
    list_cursos = []
    if codigo:
        curso = CursoScraping(codigo)
        curso.save_cursos()
    cursos = Curso.objects.values_list('codigo', 'nombre', 'electivo', 'credito')
    return JsonResponse(list(cursos), safe=False)
