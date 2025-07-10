from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

from project.settings import SERVIDOR
# CONSULTAS
from django.db.models import Q

# Notificaciones
from scripts.notificaciones.creacion_notificacion import creacion_notificacion_administradores

# URLS
from apps.actividades.utils import build_notificacion_especificaciones

# ENVIO DE MENSAJE DE EMAIL PARA DARLE LA BIENVENIDA A UN CLIENTE
def send_email_welcome_customer(customer):
    # Envio de correos
    # Mensaje de bienvendia a un cliente a la empresa
   
    template = get_template('email/welcome_message.html')
    
    context = {
        'nombre_usuario': customer.get_full_name(),
        
    }

    content = template.render(context)

    email = EmailMultiAlternatives(
        'BIENVENIDO',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        ['{}'.format(customer.email)]
    )
    email.attach_alternative(content, 'text/html')

    if SERVIDOR:
        email.send()

# NOTIFICAR A TODOS LOS ADMINISTRADORES DE UN NUEVO CLIENTE A LA EMPRESA
def send_email_new_customer(customer):
    # Envio de correos
    # Mensaje de bienvenida a un cliente a la empresa
    template = get_template('email/message_new_customer.html')
    
    context = {
        'nombre_usuario': customer.get_full_name(),  # Llamar al método correctamente
        'email':customer.email,
        'date':customer.creation_date,
        'code':customer.customer_code,
    }

    
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(Q(rol__role_name='Administrador'), status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        'CLIENTE NUEVO',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')
    
    if SERVIDOR and usuarios_email:
        email.send()
        print('Generando alerta!')

       
        especificaciones = build_notificacion_especificaciones(

            view_name='customers:detail',
            kwargs={'customer_code': customer.customer_code},
            extra_data={
                'contenido':f'''
Detalles del Cliente:
Nombre: { customer.first_name}
Correo Electronico: {customer.email}
Codigo del Cliente: {customer.customer_code}
'''
            }
            
           
        )

        mensaje = {
            'title':f'Registro de Cliente Nuevo. 😏',
            'message':f'Se ha registrado un cliente nuevo',
            'especificaciones':especificaciones
        }
        creacion_notificacion_administradores(mensaje)
    
