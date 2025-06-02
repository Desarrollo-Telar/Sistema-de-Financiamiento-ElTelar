from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User




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
    email.send()




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
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True, status=True)]

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
    email.send()

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
    email.send()

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
    email.send()

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
    email.send()

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
def send_email_update_of_quotas(cuotas):
    template = get_template('email/update_of_quotas.html')
    full_url = 'https://www.ii-eltelarsa.com'
    context = {
        'cuotas':cuotas,
        'full_url':full_url,
        
    }
    # Recolectar correos electrónicos de todos los superusuarios
    usuarios_email = [user.email for user in User.objects.filter(is_superuser=True, status=True)]

    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'ALERTA CUOTAS ACTUALIZADAS',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')
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
    usuarios_email = ['eloicx@gmail.com','iieltelarsa@gmail.com']

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
    email.send()