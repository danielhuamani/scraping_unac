# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unac', '0004_auto_20170625_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notas',
            name='anio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='anio_set', to='unac.Anio'),
        ),
    ]
