# Generated by Django 5.0.4 on 2025-06-23 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0003_permiso_remove_role_permissions_delete_userrole'),
        ('users', '0004_remove_user_rol_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rol_old',
            field=models.CharField(blank=True, choices=[('Administrador', 'Administrador'), ('Administradora', 'Administradora'), ('Programador', 'Programador'), ('Programadora', 'Programadora'), ('Secretaria', 'Secretaria'), ('Secretario', 'Secretario'), ('Contador', 'Contador'), ('Contadora', 'Contadora')], default='Administrador', max_length=50, null=True, verbose_name='Rol de Usuario'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='roles.role'),
        ),
    ]
