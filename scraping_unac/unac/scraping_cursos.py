# from django.conf import settings
import requests
from bs4 import BeautifulSoup
from .models import (Curso, Ciclo, Alumnos, Notas, Anio, Escuela)


class Scraping(object):
    """docstring for CursoScraping"""
    UNAC_URL = "http://oraa.unac.edu.pe"
    RECORD_ACADEMICO = "http://oraa.unac.edu.pe/record_notas_re.asp"
    session =    ''
    codigo = ''
    electivo = '(E)'
    escuela = ''

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

    def get_data(self):
        result = self.get_result_page()
        alumno = self.get_save_alumno(result)
        if alumno:
            self.save_cursos(result)
            self.save_notas(result, alumno)
        else:
            print("eorrrro")
        return True

    def get_escuela(self, code):
        print ('codigo', code)
        escuela, created = Escuela.objects.get_or_create(codigo=code)

        return escuela

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

    def save_notas(self, html, alumno):
        alumno = alumno
        print (alumno)
        result = html
        for tr in result.select('tr[bgcolor="WHITE"]'):

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
        escuela = self.get_escuela(52)
        print (type(escuela))
        try:
            data_html = result.select('table[width="75%"] strong')[0].text
            alumno = " ".join(data_html.split(':')[1].split("-")[:3])
            try:
                print (self.codigo)
                alumno = Alumnos(
                    codigo=self.codigo, alumno=alumno, escuela=escuela)
                alumno.save()
            except Exception as e:
                print (e)
                print ("get", self.codigo)
                try:
                    alumno = Alumnos.objects.get(codigo=self.codigo)
                except Exception as e:
                    alumno = None
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
