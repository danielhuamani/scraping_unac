# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumnos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Alumnoss',
                'verbose_name': 'Alumnos',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Curso')),
                ('codigo', models.CharField(max_length=120, unique=True, verbose_name='Codigo')),
                ('credito', models.IntegerField(verbose_name='Credito')),
                ('electivo', models.BooleanField(default=False, verbose_name='Electivo')),
            ],
            options={
                'verbose_name_plural': 'Cursos',
                'verbose_name': 'Curso',
            },
        ),
    ]
