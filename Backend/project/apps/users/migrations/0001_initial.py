# Generated by Django 5.0.4 on 2024-06-26 20:51

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('type_identification', models.CharField(choices=[('DPI', 'DPI'), ('PASAPORTE', 'PASAPORTE'), ('OTRO', 'OTRO')], default='DPI', max_length=50, verbose_name='Tipo de Identificación')),
                ('identification_number', models.CharField(max_length=15, unique=True, verbose_name='Número de Identificación')),
                ('telephone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('gender', models.CharField(choices=[('MASCULINO', 'MASCULINO'), ('FEMENINO', 'FEMENINO')], default='MASCULINO', max_length=50, verbose_name='Género')),
                ('user_code', models.CharField(max_length=25, unique=True, verbose_name='Código de Usuario')),
                ('nationality', models.CharField(default='Guatemala', max_length=75, verbose_name='Nacionalidad')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='users/profile_pics/', verbose_name='Foto de Perfil')),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Administradora', 'Administradora'), ('Programador', 'Programador'), ('Programadora', 'Programadora'), ('Secretaria', 'Secretaria'), ('Secretario', 'Secretario'), ('Contador', 'Contador'), ('Contadora', 'Contadora')], max_length=50, verbose_name='Rol de Usuario')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]