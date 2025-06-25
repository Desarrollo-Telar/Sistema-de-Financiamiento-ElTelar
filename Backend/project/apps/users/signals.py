# SIGNALS
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# TIEMPO
from datetime import datetime
from django.utils import timezone

# MODELO
from .models import User, PermisoUsuario
from apps.roles.models import Role, Permiso
from apps.customers.models import CreditCounselor
from rest_framework.authtoken.models import Token

import random


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    
    DESARROLLADOR = Role.objects.filter(role_name='Programador').first()
    ADMINISTRADOR = Role.objects.filter(role_name='Administrador').first()
    SECRETARIA = Role.objects.filter(role_name='Secretari@').first()
    ASESORCREDITO = Role.objects.filter(role_name='Asesor de Crédito').first()

    if instance.rol == DESARROLLADOR or instance.rol == ADMINISTRADOR:
        # Obtener todos los permisos existentes
        todos_los_permisos = Permiso.objects.all()

        # Obtener los permisos que ya tiene el usuario (solo los IDs)
        permisos_existentes_ids = PermisoUsuario.objects.filter(user=instance).values_list('permiso_id', flat=True)

        # Filtrar permisos que aún no tiene
        permisos_faltantes = todos_los_permisos.exclude(id__in=permisos_existentes_ids)

        # Asignar solo los permisos faltantes
        for permiso in permisos_faltantes:
            PermisoUsuario.objects.create(user=instance, permiso=permiso)

    elif instance.rol == SECRETARIA:
        # Obtener todos los permisos existentes
        todos_los_permisos = Permiso.objects.all()

        # Obtener los permisos que ya tiene el usuario (solo los IDs)
        permisos_existentes_ids = PermisoUsuario.objects.filter(user=instance).values_list('permiso_id', flat=True)

        # Filtrar permisos que aún no tiene
        permisos_faltantes = todos_los_permisos.exclude(id__in=permisos_existentes_ids)
        


    elif instance.rol == ASESORCREDITO:
        # CREACION DE REGISTRO DE ASESOR DE CREDITO
        verificar_asesor = CreditCounselor.objects.filter(usuario=instance).first()

        if verificar_asesor is not None:
            return f'Este usuario ya esta registrado como asesor'
        
        # CREACION DE REGISTRO DE ASESOR DE CREDITO        
        CreditCounselor.objects.create(
            usuario=instance,
            nombre=instance.first_name,
            apellido=instance.last_name,
            type_identification = instance.type_identification,
            identification_number = instance.identification_number,
            telephone = instance.telephone,
            email = instance.email,
            gender = instance.gender,
            nit = instance.nit
        )

    else:
        # Si al modificar o al quitar el rol, se le eliminar los permisos ya otorgados hasta el momento

        # Obtener todos los permisos que ya tiene el usuario
        print(f'Eliminacion de permisos')
        permisos_existentes = PermisoUsuario.objects.filter(user=instance)

        for permiso in permisos_existentes:
            permiso.delete()

            



# Funcion clave para la generacion de codigos de usuario, luego de haberse creado
@receiver(pre_save, sender=User)
def set_user_code(sender, instance, *args, **kwargs):
    if instance.user_code == '':
        # Obtiene la fecha y hora actual
        current_date = datetime.now()

        # Extrae el año de la fecha actual
        current_year = current_date.year  

        # Formato al codigo de usuario
        user_code_base = f'{current_year}-'

        # Contador
        counter = 1

        # Base final del codigo
        # Ejemplo: 2024-1
        user_code = f'{user_code_base}{counter}'

        # Verificar si no existe un codigo igual, si no generar uno nuevo
        while User.objects.filter(user_code=user_code).exists():
            counter += 1
            user_code = f'{user_code_base}{counter}'
            print(instance.user_code)

        # Guardar informacion
        instance.user_code = user_code

#Funcion clave para guardar el nombre de usuario utilizando el email registrado
@receiver(pre_save, sender=User)
def set_username(sender, instance, *args, **kwargs):
    if not instance.username: # Verifica si el username está vacío
        instance.username = instance.email # Usa el email como username si está vacío