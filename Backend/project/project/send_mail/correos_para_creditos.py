from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

# TIEMPO
from datetime import datetime,timedelta

from project.settings import SERVIDOR

# CONSULTAS
from django.db.models import Q

# Notificaciones
from scripts.notificaciones.creacion_notificacion import creacion_notificacion_administrador_secretaria,creacion_notificacion_administradores

# URLS
from apps.actividades.utils import build_notificacion_especificaciones

# MENSAJE DE CREDITO NUEVO
def send_email_new_credit(models):
    template = get_template('email/new_credit.html')
    context = {
        'object_list':models,
    }
    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Recolectar correos electrónicos de todos los usuarios activos
    usuarios_email = [user.email for user in User.objects.filter(Q(rol__role_name='Administrador'), status=True)]
    #usuarios_email.append(models.cliente.email)
    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'REGRISTRO DE UN NUEVO CREDITO',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR and usuarios_email:
        email.send()

        especificaciones = build_notificacion_especificaciones(

            view_name='financings:detail_credit',
            kwargs={'id': models.id}
           
        )

        mensaje = {
            'title':'Registro de un Credito Nuevo',
            'message':'Se ha registrado un nuevo credito dentro de la plataforma.',
            'especificaciones':especificaciones
        }
        creacion_notificacion_administradores(mensaje)

# MENSAJES DE ALERTAS PARA LOS PARA LOS ADMINISTRADORES, Y NOTIFICACION PARA SECRETARI@
# ESTE MENSAJE ES PARA NOTIFICAR QUE CUOTAS HAN LLEGADO A SU FECHA DE VENCIMIENTO
def send_email_next_update_of_quotas(cuotas):
    template = get_template('email/quotas_defeated.html')
    dia = datetime.now().date()
    hoy = datetime.now() 
    hasta = hoy + timedelta(days=16)
    
    full_url = 'https://www.ii-eltelarsa.com'
    context = {
        'cuotas':cuotas,
        'full_url':full_url,
        'actualizacion':hasta.date()
        
    }
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(Q(rol__role_name='Administrador')| Q(rol__role_name='Programador'), status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'Cuotas A Fecha de Vencimiento - {dia}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR and usuarios_email:
        email.send()
        especificaciones = build_notificacion_especificaciones(

            view_name='financings:filter_credito_fecha_vencimiento_hoy'
            
           
        )

        mensaje = {
            'title':'Cuotas con Fecha Vencimiento Hoy',
            'message':'Las siguientes cuotas han llegado a su fecha de vencimiento',
            'especificaciones':especificaciones
        }
        creacion_notificacion_administrador_secretaria(mensaje)
        

# MENSAJES DE ALERTAS PARA LOS PARA LOS ADMINISTRADORES, Y NOTIFICACION PARA SECRETARI@
# ESTE MENSAJE ES PARA NOTIFICAR QUE CUOTAS HAN LLEGADO A SU FECHA LIMITE
def send_email_update_of_quotas(cuotas):
    template = get_template('email/update_of_quotas.html')
    dia = datetime.now().date()
    
    
    full_url = 'https://www.ii-eltelarsa.com'
    context = {
        'cuotas':cuotas,
        'full_url':full_url
        
        
    }
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(Q(rol__role_name='Administrador')| Q(rol__role_name='Programador'), status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'Actualizacion de Cuotas  Por Fecha Limite - {dia}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR and usuarios_email:
        email.send()
        especificaciones = build_notificacion_especificaciones(

            view_name='financings:filter_credito_fecha_limite_hoy'
            
           
        )

        mensaje = {
            'title':'Cuotas con Fecha Limite Hoy',
            'message':'Las siguientes cuotas han llegado a su fecha limite',
            'especificaciones':especificaciones
        }
        creacion_notificacion_administrador_secretaria(mensaje)
        
        

# MENSAJES DE ALERTAS PARA LOS PARA LOS ADMINISTRADORES
# ESTE MENSAJE ES PARA NOTIFICAR QUE CUOTAS ESTAN PROXIMOS A VENCERSE
def send_email_quotas_for_change(cuotas, hoy, hasta):
    template = get_template('email/quotas_for_change.html')
    dia = datetime.now().date()
    full_url = 'https://www.ii-eltelarsa.com'
    context = {
        'cuotas':cuotas,
        'full_url':full_url,
        'hoy':hoy,
        'hasta':hasta
        
    }
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(Q(rol__role_name='Administrador')| Q(rol__role_name='Programador'), status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'Proximas Cuotas En Llegar a su Fecha de Vencimiento, TOMAR NOTA - {dia} ',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')
    
    if SERVIDOR and usuarios_email:
        email.send()