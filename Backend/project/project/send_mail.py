from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

def send_email_code_verification(user, code):
    template = get_template('email/send_code.html')
    user_mail = user.email
    context = {
        'user':user,
        'code':code,
    }

    content = template.render(context)
 
    email = EmailMultiAlternatives(
        'Codigo de verificación',
        'EL Telar',
        settings.EMAIL_HOST_USER,
        ['{}'.format(user_mail)]
    )
    email.attach_alternative(content, 'text/html')
    email.send()


def send_email_welcome_customer(customer):
    # Envio de correos
    # Mensaje de bienvendia a un cliente a la empresa
    template = get_template('email/welcome_message.html')
    
    context = {
        'nombre_usuario': customer.get_full_name(),
        
    }

    content = template.render(context)

    email = EmailMultiAlternatives(
        'Bienvenido',
        'EL Telar',
        settings.EMAIL_HOST_USER,
        ['{}'.customer.email]
    )
    email.attach_alternative(content, 'text/html')
    email.send()

def send_email_new_customer(customer):
    # Envio de correos
    # Mensaje de bienvenida a un cliente a la empresa
    template = get_template('email/message_new_customer.html')
    
    context = {
        'nombre_usuario': customer.get_full_name(),  # Llamar al método correctamente
        'email':customer.email,
        'date':customer.creation_date
    }

    
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        'Cliente Nuevo',
        'EL Telar',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')
    email.send()