from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

from project.settings import SERVIDOR

# CONSULTAS
from django.db.models import Q

# ENVIO DE MENSAJE DE EMAIL PARA CODIGO DE VERIFICACION

def send_email_code_verification(user, code):
    
  
    template = get_template('email/send_code.html')
    user_mail = user.email
    context = {
        'user':user,
        'code':code,
    }

    content = template.render(context)
 
    email = EmailMultiAlternatives(
        'CODIGO DE VERIFICACIÓN',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        ['{}'.format(user_mail)]
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR:
        email.send()

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
def send_email_user_conect_or_disconect(usuario, hora, estado):
    template = get_template('email/user_conect.html')
    context = {
        'user':usuario,
        'hora':hora,
        'estado':estado,
        
    }
    # Recolectar correos electrónicos de todos los superusuarios
    
    usuarios_email = [user.email for user in User.objects.filter(Q(rol__role_name='Programador'), status=True)]


    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'USUARIO HA {estado}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')
    
    if SERVIDOR and usuarios_email:
        email.send()

