# Generated by Django 2.2.28 on 2024-01-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20240111_0913'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configurations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
