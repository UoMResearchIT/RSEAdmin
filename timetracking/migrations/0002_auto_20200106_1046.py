# Generated by Django 3.0 on 2020-01-06 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetracking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timesheetentry',
            old_name='person',
            new_name='rse',
        ),
    ]