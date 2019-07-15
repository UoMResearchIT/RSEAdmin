# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-15 10:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rse', '0003_project_polymorphic_ctype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='start',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]