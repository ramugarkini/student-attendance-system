# Generated by Django 2.2.28 on 2024-01-11 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0013_enrollmentyears_current_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrollmentyears',
            old_name='current_year',
            new_name='current_academic_year',
        ),
    ]
