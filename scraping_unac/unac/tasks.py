from __future__ import absolute_import
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from celery import shared_task
from logging import getLogger
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task, task
from celery.task.schedules import crontab
from unac.scraping_cursos import Scraping

logger = get_task_logger(__name__)
log = getLogger('django')


@task(name="create_alumno")
def create_alumno(code):
    logger.info("*** START: Creando agenda ***")
    curso = Scraping(code)
    curso.get_escuela(52)
    curso.get_data()

    logger.info("*** END: Agenda ***")
