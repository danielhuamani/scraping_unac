
from django.core.management.base import BaseCommand

import json
import csv
from unac.tasks import create_alumno


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data_csv/codigos/sistemas_cod_csv.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                create_alumno.delay(row[0])