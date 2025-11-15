# Modelos
from apps.actividades.models import Notification
from apps.users.models import User



def creando_notificacion(lista, mensaje, sucursal=None):
    # Funcion que se encarga de generar el registro de la notificacion
    for usuario in lista:
        Notification.objects.create(
            user=usuario,
            title=mensaje['title'],
            message=mensaje['message'],
            especificaciones=mensaje['especificaciones']
        )

def creacion_notificacion_administradores(mensaje, sucursal = None):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador']

    if sucursal is not None:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles,
            sucursal = sucursal
        )
    else:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles
        )

    creando_notificacion(usuarios, mensaje, sucursal)

def creacion_notificacion(roles, mensaje, sucursal = None): 
    if sucursal is not None:

        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles,
            sucursal = sucursal
        )
    else:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles
        )


    creando_notificacion(usuarios, mensaje)

def creacion_notificacion_todos(mensaje):
    # Funcion que envia la notificacion a todos los usuarios
    usuarios = User.objects.filter(
        status=True
    )
    creando_notificacion(usuarios, mensaje)

def creacion_notificacion_administrador_secretaria(mensaje, sucursal = None):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador', 'Secretari@']

    if sucursal is not None:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles,
            sucursal = sucursal
        )
    else:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles
        )

    creando_notificacion(usuarios, mensaje, sucursal)

def creacion_notificacion_administrador_asesor_credito(mensaje, sucursal=None):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador', 'Asesor de Crédito']

    if sucursal is not None:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles,
            sucursal = sucursal
        )
    else:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles
        )

    creando_notificacion(usuarios, mensaje)

def creacion_notificacion_administrador_asesor_credito_secretaria(mensaje, sucursal= None):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador', 'Asesor de Crédito','Secretari@']

    if sucursal is not None:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles,
            sucursal = sucursal
        )
    else:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name__in=roles
        )

    creando_notificacion(usuarios, mensaje)


def creacion_notificacion_secre(mensaje, sucursal = None):
    # Funcion para que se envie a los secres
    
    if sucursal is not None:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name="Secretari@",
            sucursal = sucursal
        )
    else:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name="Secretari@"
        )

    creando_notificacion(usuarios, mensaje)

def creacion_notificacion_asesores(mensaje, sucursal = None):
    # Funcion para que se envie a los Asesor de Crédito
    if sucursal is not None:

        usuarios = User.objects.filter(
            status=True,
            rol__role_name="Asesor de Crédito",
            sucursal = sucursal
        )
    else:
        usuarios = User.objects.filter(
            status=True,
            rol__role_name="Asesor de Crédito"
        )


    creando_notificacion(usuarios, mensaje)