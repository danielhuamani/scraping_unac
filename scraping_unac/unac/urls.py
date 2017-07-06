from django.conf.urls import url
from .views import (cargar_data, index, alumnos, notas, generate_csv_data_format_1)

urlpatterns = [
    url(r"^cargar_data/$", cargar_data, name="cargar_data"),
    url(r"^$", index, name="index"),
    url(r"^alumnos/$", alumnos, name="alumnos"),
    url(r"^alumnos/(?P<pk>\d+)/$", notas, name="notas"),
    url(r"^generate_csv_data_format_1/$", generate_csv_data_format_1, name="generate_csv_data_format_1"),

]
