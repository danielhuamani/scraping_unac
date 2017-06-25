# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unac', '0006_notas_modificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='anio',
            name='creatdo',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AddField(
            model_name='notas',
            name='creatdo',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='notas',
            name='modificado',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha'),
        ),
    ]