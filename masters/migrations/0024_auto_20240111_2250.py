# Generated by Django 2.2.28 on 2024-01-11 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0023_auto_20240111_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYears',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year'), ('G', 'Graduated')], default='1', max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='enrollmentyears',
            name='current_academic_year',
        ),
        migrations.AlterField(
            model_name='subjects',
            name='academic_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='masters.AcademicYears'),
        ),
        migrations.AddField(
            model_name='enrollmentyears',
            name='academic_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='masters.AcademicYears'),
            preserve_default=False,
        ),
    ]
