from django.conf.urls import url
from .views import (cursos, )

urlpatterns = [
     url(r"^cursos/$", cursos, name="cursos"),



 ]
