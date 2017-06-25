from django.conf.urls import url
from .views import (cargar_data, index, alumnos, notas)

urlpatterns = [
    url(r"^cargar_data/$", cargar_data, name="cargar_data"),
    url(r"^$", index, name="index"),
    url(r"^alumnos/$", alumnos, name="alumnos"),
    url(r"^alumnos/(?P<pk>\d+)/$", notas, name="notas"),
 ]
