# from django.conf import settings
import requests
from bs4 import BeautifulSoup
from .models import (Curso, Ciclo, Alumnos, Notas, Anio)


class Scraping(object):
    """docstring for CursoScraping"""
    UNAC_URL = "http://oraa.unac.edu.pe"
    RECORD_ACADEMICO = "http://oraa.unac.edu.pe/record_notas_re.asp"
    session =    ''
    codigo = ''
    electivo = '(E)'

    def __init__(self, codigo):
        super(Scraping, self).__init__()
        self.codigo = codigo
        self.session = requests.Session()

    # def get_session(self):

    def post_page_record(self):

        return self.session.post(
            self.RECORD_ACADEMICO, data={'codigo': self.codigo})

    def parse_html(self, html):
        return BeautifulSoup(html.content, 'html.parser')

    def get_result_page(self):
        result = self.parse_html(self.post_page_record())
        return result

    def get_data_cursos(self, html):
        result = html

        for tr in result.select('tr[bgcolor="WHITE"]'):
            ciclo = tr.find_all('td')[5].text
            ciclo, created = Ciclo.objects.get_or_create(ciclo=ciclo)
            curso = {
                'ciclo': ciclo,
                'codigo': tr.find_all('td')[0].text,
                'nombre': tr.find_all('td')[1].text,
                'credito': tr.find_all('td')[2].text,
                'electivo': self.electivo in tr.find_all('td')[1].text
            }
            yield curso

    # def save_ciclo(self):
    #     for

    def get_data(self):
        result = self.get_result_page()
        self.get_save_alumno(result)
        self.save_cursos(result)
        self.save_notas(result)
        return True

    def get_curso(self, codigo, credito=None, nombre=None):
        print (codigo, credito, nombre)
        try:
            obj = Curso.objects.get(codigo=codigo)
        except Exception as e:
            obj = Curso(
                codigo=codigo,
                credito=credito,
                nombre=nombre
            )
            obj.save()
        return obj

    def get_save_anio(self, html):
        result = html

        for tr in result.select('td[align="CENTER"]'):
            anio = tr.text.split(" ")[1]
            if ("B" in anio or "A" in anio):
                obj, create = Anio.objects.get_or_create(anio=anio)
        return True

    def save_notas(self, html):
        alumno = self.get_save_alumno(html)
        print (alumno)
        result = html
        for tr in result.select('tr[bgcolor="WHITE"]'):

            print (tr.find_all('td')[4].text)
            try:
                curso = self.get_curso(
                    tr.find_all('td')[0].text,
                    tr.find_all('td')[2].text,
                    tr.find_all('td')[1].text
                )
                nota = Notas(
                    alumno=alumno,
                    nota=tr.find_all('td')[4].text,
                    curso=curso
                )
                nota.save()

            except Exception as e:
                raise

    def get_save_alumno(self, html):
        result = html

        try:

            data_html = result.select('table[width="75%"] strong')[0].text
            alumno = " ".join(data_html.split(':')[1].split("-")[:3])
            try:
                print (self.codigo)
                alumno = Alumnos(codigo=self.codigo, alumno=alumno)
                alumno.save()
            except Exception as e:
                print ("get", self.codigo)
                alumno = Alumnos.objects.get(codigo=self.codigo)
            return alumno
        except Exception as e:
            alumno = None
            return alumno


    def save_cursos(self, html):
        for cur in self.get_data_cursos(html):
            try:
                Curso(**cur).save()
            except Exception as e:
                pass
