from django.db import models

# Create your models here.


class Ciclo(models.Model):
    ciclo = models.CharField('ciclo', max_length=120)
    nombre = models.CharField("Curso", max_length=120, blank=True)

    class Meta:
        verbose_name = "Ciclo"
        verbose_name_plural = "Ciclos"

    def __str__(self):
        return self.ciclo


class Curso(models.Model):
    ciclo = models.ForeignKey("Ciclo", related_name="ciclo_set")
    nombre = models.CharField("Curso", max_length=120)
    codigo = models.CharField("Codigo", max_length=120, unique=True)
    credito = models.IntegerField("Credito")
    electivo = models.BooleanField("Electivo", default=False)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre


class Alumnos(models.Model):
    creado = models.DateTimeField("Fecha", auto_now_add=True, null=True)
    codigo = models.CharField("Codigo", max_length=120, unique=True)
    alumno = models.CharField("Alumno", max_length=120)

    class Meta:
        verbose_name = "Alumnos"
        verbose_name_plural = "Alumnoss"

    def __str__(self):
        return self.alumno


class Anio(models.Model):
    creado = models.DateTimeField("Fecha", auto_now_add=True, null=True)
    anio = models.CharField("Anio", unique=True, max_length=120)

    class Meta:
        verbose_name = "Anio"
        verbose_name_plural = "Anios"

    def __str__(self):
        return self.anio


class Notas(models.Model):
    creatdo = models.DateTimeField("Fecha", auto_now_add=True, null=True)
    modificado = models.DateTimeField("Fecha", auto_now=True, null=True)
    alumno = models.ForeignKey("Alumnos", related_name="alumnos_set")
    curso = models.ForeignKey("Curso", related_name="cursos_set")
    nota = models.CharField("Nota", max_length=120)
    anio = models.ForeignKey("Anio", related_name="anio_set", null=True)

    class Meta:
        verbose_name = "Notas"
        verbose_name_plural = "Notass"
        unique_together = ('alumno', 'curso', 'anio')

    def __str__(self):

        return "anio {0}".format(self.nota)
