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

from django.db.models.signals import pre_save
from django.dispatch import receiver



@receiver(post_save, sender=PermisoUsuario)
def despues_de_guardar(sender, instance, created, **kwargs):
    if created:
        print("🆕 Registro nuevo guardado")
        permiso_otorgado = PermisoUsuario.objects.filter(user=instance.user, permiso=instance.permiso).count()
        if permiso_otorgado > 1:
            instance.delete()

    else:
        print("🔄 Registro existente actualizado")
        permiso_otorgado = PermisoUsuario.objects.filter(user=instance.user, permiso=instance.permiso).count()
        if permiso_otorgado > 1:
            instance.delete()




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

        # Listado de Permisos Como Rol de Secretaria
        permisos_secretaria_generales = [
            'puede_ver_perfil_usuario',

            # -------- CREAR
            'puede_crear_informacion_personal_cliente',
            'puede_crear_informacion_laboral_cliente',
            #'puede_crear_informacion_destino_credito',
            'puede_crear_direccion',
            'puede_crear_referencias',
            'puede_subir_imagenes',
            'puede_subir_archivos',
            'puede_crear_informacion_credito',
            'puede_crear_registro_desembolso',
            'puede_crear_registro_garantia',
            'puede_crear_boleta_pago',
            
            # ------- EDITAR
            'puede_editar_informacion_laboral_cliente',

            # ------- DESCARGAR
            'puede_descargar_archivos',
            'puede_descargar_imagenes',
            'puede_descargar_plan_de_pagos_de_credito',
            'puede_descargar_estado_cuenta_credito',
            'puede_descargar_informe_de_cuotas',
            'puede_descargar_imagen_boleta_pago',

            # -------- VISUALIZAR
            'puede_visualizar_el_registro_clientes',
            'puede_ver_registros_credito',
            'puede_ver_listado_plan_pagos_de_credito',
            'puede_ver_listado_de_cuotas_vencidas',
            'puede_ver_listado_de_garantias_del_credito',
            'puede_ver_listado_de_desembolsos_aplicados_del_credito',
            'puede_ver_registros_boletas_pagos',
            

            # -------- CONSULTAR
            'puede_realizar_consultas_informacion_credito',
            'puede_realizar_consultar_de_clientes',
            'puede_consultar_cuota_por_cobrar',
            'puede_realizar_consultas_boleta_pagos',
            

            # ------- DETALLE
            'puede_visualizar_detalle_cliente',
            'puede_visualizar_detalle_informacion_laboral_cliente',
            'puede_visualizar_detalle_informacion_destino_credito',
            'puede_ver_detalle_direccion',
            'puede_ver_detalle_referencias',
            'puede_ver_detalle_credito',
            'puede_ver_detalle_garantia',
            'puede_ver_detalle_desembolso',
            'puede_ver_detalle_estado_cuenta_credito',
            'puede_ver_detalle_boleta_pago',
            'puede_ver_detalle_recibo_pago',  
            
        ]

        # Asignar solo los permisos faltantes
        for permiso in permisos_faltantes:
            if permiso.codigo_permiso in permisos_secretaria_generales:
                PermisoUsuario.objects.create(user=instance, permiso=permiso)
        


    elif instance.rol == ASESORCREDITO:
        # Obtener todos los permisos existentes
        todos_los_permisos = Permiso.objects.all()

        # Obtener los permisos que ya tiene el usuario (solo los IDs)
        permisos_existentes_ids = PermisoUsuario.objects.filter(user=instance).values_list('permiso_id', flat=True)

        # Filtrar permisos que aún no tiene
        permisos_faltantes = todos_los_permisos.exclude(id__in=permisos_existentes_ids)

        # Listado de Permisos Como Rol de Secretaria
        permisos_secretaria_generales = [
            'puede_ver_perfil_usuario',
            # ----- CREAR ---------
            'puede_crear_informacion_personal_cliente',
            'puede_crear_informacion_laboral_cliente',
            'puede_crear_direccion',
            'puede_crear_referencias',
            'puede_subir_imagenes',
            'puede_subir_archivos',
            'puede_crear_registro_desembolso',
            'puede_crear_registro_garantia',
            #'puede_crear_informacion_credito',

            # ------- CONSULTAS -------
            'puede_realizar_consultar_de_clientes',
            #'puede_realizar_consultas_informacion_credito',
            
            
            # ------ VISUALIZAR
            'puede_visualizar_el_registro_clientes',
            'puede_visualizar_detalle_cliente',
            'puede_visualizar_detalle_informacion_laboral_cliente',
            'puede_visualizar_detalle_informacion_destino_credito',
            
            'puede_ver_registros_credito',
            'puede_ver_listado_plan_pagos_de_credito',
            'puede_ver_listado_de_cuotas_vencidas',
            'puede_ver_listado_de_garantias_del_credito',
            'puede_ver_listado_de_desembolsos_aplicados_del_credito',

            # -------- DETALLE --------
            'puede_ver_detalle_direccion',
            'puede_ver_detalle_referencias',
            'puede_ver_detalle_credito',
            'puede_ver_detalle_garantia',
            'puede_ver_detalle_desembolso',
            'puede_ver_detalle_estado_cuenta_credito',

            # --------- DESCARGAR -
            'puede_descargar_imagenes',
            'puede_descargar_archivos',
            
            'puede_descargar_plan_de_pagos_de_credito',
            'puede_descargar_estado_cuenta_credito',
            'puede_descargar_informe_de_cuotas',
           
          

            
        ]

        # Asignar solo los permisos faltantes
        for permiso in permisos_faltantes:
            if permiso.codigo_permiso in permisos_secretaria_generales:
                PermisoUsuario.objects.create(user=instance, permiso=permiso)

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