# Modelos
from apps.actividades.models import Notification
from apps.users.models import User



def creando_notificacion(lista, mensaje):
    # Funcion que se encarga de generar el registro de la notificacion
    for usuario in lista:
        Notification.objects.create(
            user=usuario,
            title=mensaje['title'],
            message=mensaje['message'],
            especificaciones=mensaje['especificaciones']
        )

def creacion_notificacion_administradores(mensaje):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador']

    usuarios = User.objects.filter(
        status=True,
        rol__role_name__in=roles
    )

    creando_notificacion(usuarios, mensaje)

def creacion_notificacion(roles, mensaje): 
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

def creacion_notificacion_administrador_secretaria(mensaje):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador', 'Secretari@']

    usuarios = User.objects.filter(
        status=True,
        rol__role_name__in=roles
    )

    creando_notificacion(usuarios, mensaje)

def creacion_notificacion_administrador_asesor_credito(mensaje):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador', 'Asesor de Crédito']

    usuarios = User.objects.filter(
        status=True,
        rol__role_name__in=roles
    )

    creando_notificacion(usuarios, mensaje)

def creacion_notificacion_administrador_asesor_credito_secretaria(mensaje):
    # Funcion para quien va las notificaciones
    roles = ['Administrador', 'Programador', 'Asesor de Crédito','Secretari@']

    usuarios = User.objects.filter(
        status=True,
        rol__role_name__in=roles
    )

    creando_notificacion(usuarios, mensaje)


def creacion_notificacion_secre(mensaje):
    # Funcion para que se envie a los secres
    usuarios = User.objects.filter(
        status=True,
        rol__role_name="Secretari@"
    )

    creando_notificacion(usuarios, mensaje)

def creacion_notificacion_asesores(mensaje):
    # Funcion para que se envie a los Asesor de Crédito
    usuarios = User.objects.filter(
        status=True,
        rol__role_name="Asesor de Crédito"
    )

    creando_notificacion(usuarios, mensaje)