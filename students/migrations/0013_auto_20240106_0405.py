# Generated by Django 2.2.28 on 2024-01-06 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_auto_20240106_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='masters.Department'),
        ),
    ]
