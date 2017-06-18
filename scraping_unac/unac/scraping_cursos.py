# from django.conf import settings
import requests
from bs4 import BeautifulSoup
from .models import Curso, Ciclo


class CursoScraping(object):
    """docstring for CursoScraping"""
    UNAC_URL = "http://oraa.unac.edu.pe"
    RECORD_ACADEMICO = "http://oraa.unac.edu.pe/record_notas_re.asp"
    session = ''
    codigo = ''
    electivo = '(E)'

    def __init__(self, codigo):
        super(CursoScraping, self).__init__()
        self.codigo = codigo

    def get_session(self):
        self.session = requests.Session()

    def post_page_record(self):

        return self.session.post(
            self.RECORD_ACADEMICO, data={'codigo': self.codigo})

    def parse_html(self, html):
        return BeautifulSoup(html.content, 'html.parser')

    def get_data_cursos(self):
        result = self.parse_html(self.post_page_record())
        for tr in result.select('tr[bgcolor="WHITE"]'):
            curso = {
                'codigo': tr.find_all('td')[0].text,
                'nombre': tr.find_all('td')[1].text,
                'credito': tr.find_all('td')[2].text,
                'electivo': self.electivo in tr.find_all('td')[1].text
            }
            yield curso

    def save_cursos(self):
        for cur in self.get_data_cursos():
            try:
                Curso(**cur).save()
            except Exception as e:
                pass
