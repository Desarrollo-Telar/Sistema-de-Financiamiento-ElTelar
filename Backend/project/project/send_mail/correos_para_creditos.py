from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

# TIEMPO
from datetime import datetime,timedelta

from project.settings import SERVIDOR

# MENSAJE DE CREDITO NUEVO
def send_email_new_credit(models):
    template = get_template('email/new_credit.html')
    context = {
        'object_list':models,
    }
    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Recolectar correos electrónicos de todos los usuarios activos
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True, status=True)]
    #usuarios_email.append(models.cliente.email)
    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'REGRISTRO DE UN NUEVO CREDITO',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR:
        email.send()

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
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
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True, status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'ESTAS CUOTAS HOY LLEGARON A SU FECHA DE VENCIMIENTO - {dia}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR:
        email.send()

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
def send_email_update_of_quotas(cuotas):
    template = get_template('email/update_of_quotas.html')
    dia = datetime.now().date()
    
    
    full_url = 'https://www.ii-eltelarsa.com'
    context = {
        'cuotas':cuotas,
        'full_url':full_url
        
        
    }
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True, status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'ESTAS CUOTAS LLEGARON A SU FECHA LIMITE - {dia}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR:
        email.send()

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
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
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True, status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'ALERTA LAS PROXIMAS CUOTAS ESTAN A PUNTO DE VENCERSE, TOMAR NOTA - {dia} ',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')
    
    if SERVIDOR:
        email.send()