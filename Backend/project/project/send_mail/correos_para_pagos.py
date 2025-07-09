from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

from project.settings import SERVIDOR

# CONSULTAS
from django.db.models import Q

# Notificaciones
from scripts.notificaciones.creacion_notificacion import creacion_notificacion

# URLS
from apps.actividades.utils import build_notificacion_especificaciones


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

    lista_tipos = ['DESEMBOLSO', 'CREDITO']

    # Roles por defecto
    roles = ['Administrador', 'Programador']

    # Si el tipo de pago está en la lista, se agregan más roles
    if models.tipo_pago in lista_tipos:
        roles.append('Secretari@')

    # Obtener correos de usuarios activos con los roles indicados
    usuarios_email = User.objects.filter(
        rol__role_name__in=roles,
        status=True
    ).values_list('email', flat=True)
        

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
    
    if SERVIDOR and usuarios_email:
        
        #email.send()
        print('envio de notificacion')

        especificaciones = build_notificacion_especificaciones(

            view_name='financings:detalle_boleta',
            kwargs={'id': models.id},
            extra_data={
                'contenido': f'''
Numero de Referencia: { models.numero_referencia }
Monto: Q {models.Fmonto()}
Para: {models.boleta_para()}
'''
            }
            
           
        )

        emojin = '😕'

        if status == 'COMPLETADO':
            emojin = '😎'

        mensaje = {
            'title':f'ALERTA DE BOLETA. {emojin}',
            'message':f'La siguiente boleta con {models.numero_referencia} esta en status {status}',
            'especificaciones':especificaciones
        }
        creacion_notificacion(roles,mensaje)




# MENSAJES PARA EL MANEJO DE RECIBOS
def send_email_recibo(models):
    template = get_template('email/recibo.html')
    context = {
        'recibo':models,
    }
    # Renderizar el contenido del correo electrónico
    content = template.render(context)

    lista_tipos = ['DESEMBOLSO', 'CREDITO']

    # Roles por defecto
    roles = ['Administrador', 'Programador']

    # Si el tipo de pago está en la lista, se agregan más roles
    if models.pago.tipo_pago in lista_tipos:
        roles.append('Secretari@')

    # Obtener correos de usuarios activos con los roles indicados
    usuarios_email = User.objects.filter(
        rol__role_name__in=roles,
        status=True
    ).values_list('email', flat=True)

    #usuarios_email.append(models.cliente.email)
    # Crear y enviar el correo electrónico
    email = EmailMultiAlternatives(
        f'RECIBO DE {models.pago.boleta_para()}',
        'ELTELAR',
        settings.EMAIL_HOST_USER,
        usuarios_email
    )
    email.attach_alternative(content, 'text/html')

    if models.pago.registro_ficticio:
        return
    
    if SERVIDOR and usuarios_email:
        
        email.send()
        print('envio de notificacion')
        especificaciones = build_notificacion_especificaciones(

            view_name='financings:recibo',
            kwargs={'id': models.pago.id}
            
           
        )

        mensaje = {
            'title':f'Se genero un Recibo. 📋',
            'message':f'Recibo para {models.pago.boleta_para()}',
            'especificaciones':especificaciones
        }
        creacion_notificacion(roles,mensaje)
