# Generated by Django 2.2.28 on 2024-01-05 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20240102_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='year',
            new_name='enroll_year',
        ),
    ]