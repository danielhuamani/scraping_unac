# from django.conf import settings
import requests
from bs4 import BeautifulSoup
from .models import Curso, Ciclo, Alumnos


class Scraping(object):
    """docstring for CursoScraping"""
    UNAC_URL = "http://oraa.unac.edu.pe"
    RECORD_ACADEMICO = "http://oraa.unac.edu.pe/record_notas_re.asp"
    session = ''
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

    def get_data_cursos(self):
        result = self.get_result_page()
        for tr in result.select('tr[bgcolor="WHITE"]'):
            curso = {
                'codigo': tr.find_all('td')[0].text,
                'nombre': tr.find_all('td')[1].text,
                'credito': tr.find_all('td')[2].text,
                'electivo': self.electivo in tr.find_all('td')[1].text
            }
            yield curso

    # def save_ciclo(self):
    #     for

    def save_alumno(self):
        result = self.get_result_page()
        alumno = result.select('table[width="75%"] strong')[0].text
        try:
            alumno = Alumnos(codigo=self.codigo, alumno=alumno)
            alumno.save()
        except Exception as e:
            alumno = Alumnos.object.get(codigo=self.codigo)
        return alumno

    def save_cursos(self):
        for cur in self.get_data_cursos():
            try:
                Curso(**cur).save()
            except Exception as e:
                pass
