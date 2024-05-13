from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings


def send_email_welcome_customer(customer):
    # Envio de correos
    # Mensaje de bienvendia a un cliente a la empresa
    template = get_template('email/welcome_message.html')
    
    context = {
        'nombre_usuario': customer,
        
    }

    content = template.render(context)

    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'EL Telar',
        settings.EMAIL_HOST_USER,
        ['eloicx@gmail.com']
    )
    email.attach_alternative(content, 'text/html')
    email.send()

