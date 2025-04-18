# Generated by Django 5.0.4 on 2025-01-09 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=100, unique=True, verbose_name='Nombre del Rol')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.permission', verbose_name='Permisos')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idRole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rol_usuario', to='roles.role', verbose_name='Rol')),
            ],
            options={
                'verbose_name': 'Rol de Usuario',
                'verbose_name_plural': 'Roles de Usuarios',
            },
        ),
    ]
