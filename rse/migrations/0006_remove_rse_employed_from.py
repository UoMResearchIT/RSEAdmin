# Generated by Django 2.2.7 on 2019-12-02 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rse', '0005_auto_20191127_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rse',
            name='employed_from',
        ),
    ]
