# Generated by Django 2.2.28 on 2023-12-28 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.IntegerField(),
        ),
    ]
