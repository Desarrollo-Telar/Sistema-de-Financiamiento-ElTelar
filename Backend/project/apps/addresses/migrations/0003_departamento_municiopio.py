# Generated by Django 5.0.4 on 2024-11-25 23:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre del Departamento')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Municiopio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre del Municiopio')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addresses.departamento')),
            ],
            options={
                'verbose_name': 'Municiopio',
                'verbose_name_plural': 'Municipios',
            },
        ),
    ]