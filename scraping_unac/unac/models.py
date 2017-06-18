from django.db import models

# Create your models here.


class Ciclo(models.Model):
    ciclo = models.CharField('ciclo', max_length=120)
    nombre = models.CharField("Curso", max_length=120, blank=True)

    class Meta:
        verbose_name = "Ciclo"
        verbose_name_plural = "Ciclos"

    def __str__(self):
        return self.nombre


class Curso(models.Model):
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
    codigo = models.CharField("Codigo", max_length=120, unique=True)
    alumno = models.CharField("Alumno", max_length=120)

    class Meta:
        verbose_name = "Alumnos"
        verbose_name_plural = "Alumnoss"

    def __str__(self):
        pass

