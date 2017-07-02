from django.contrib import admin
from .models import Curso, Notas, Escuela
# Register your models here.


class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'electivo', 'credito']


admin.site.register(Curso, CursoAdmin)
admin.site.register(Notas)
admin.site.register(Escuela)
