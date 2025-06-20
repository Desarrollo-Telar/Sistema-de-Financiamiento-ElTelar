from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

from project.settings import SERVIDOR

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
def send_email_alert(message, status,models):
    template = get_template('email/alert_message.html')
    full_url = 'https://www.ii-eltelarsa.com'
    context = {
        'message':message,
        'full_url':full_url,
        'object':models,
        'status':status,
    }
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True, status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'ALERTA {status} PARA {models.numero_referencia}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if models.registro_ficticio:
        return
    
    if SERVIDOR:
        email.send()




# MENSAJES PARA EL MANEJO DE RECIBOS
def send_email_recibo(models):
    template = get_template('email/recibo.html')
    context = {
        'recibo':models,
    }
    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Recolectar correos electrónicos de todos los usuarios activos
    usuarios_email = [user.email for user in User.objects.filter( status=True)]
    #usuarios_email.append(models.cliente.email)
    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'RECIBO DE {models.pago.boleta_para()}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')
    
    if SERVIDOR:
        email.send()
