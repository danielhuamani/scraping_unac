# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 04:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnos',
            name='alumno',
            field=models.CharField(default='', max_length=120, verbose_name='Alumno'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alumnos',
            name='codigo',
            field=models.CharField(default='', max_length=120, unique=True, verbose_name='Codigo'),
            preserve_default=False,
        ),
    ]
