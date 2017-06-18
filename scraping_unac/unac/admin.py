from django.contrib import admin
from .models import Curso
# Register your models here.


class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'electivo', 'credito']


admin.site.register(Curso, CursoAdmin)
