from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

from project.settings import SERVIDOR

# CONSULTAS
from django.db.models import Q

# ENVIO DE MENSAJE DE EMAIL PARA CODIGO DE VERIFICACION

import logging
from django.template import TemplateDoesNotExist
from apps.actividades.utils import log_user_action, log_system_event

import traceback


def send_email_code_verification(user, code, usuario, accion):
    user_mail = user.email

    # 1. Validar que el usuario tenga un correo configurado
    if not user_mail:
        
        log_system_event(
            message=f"No se pudo enviar correo: El usuario {usuario} no tiene un email configurado.",
            level_name="WARNING",
            source="send_email_code_verification",
            category_name="Correo"
        )
        return 

    # 2. Renderizar la plantilla
    try:
        template = get_template("email/send_code.html")
        context = {"user": usuario, "code": code, "accion": accion}
        content = template.render(context)
    except TemplateDoesNotExist:
        
        log_system_event(
            message=f"No se pudo enviar correo: La plantilla 'email/send_code.html' no existe.",
            level_name="ERROR", 
            source="send_email_code_verification",
            category_name="Correo"
        )
        return 
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar la plantilla de correo: {e}",
            level_name="ERROR",
            source="send_email_code_verification",
            category_name="Correo"
        )
        return 

    # 3. Construir y enviar el correo
    try:
        email = EmailMultiAlternatives(
            subject=f"CÓDIGO DE VERIFICACIÓN: {code}",
            body=f"Su código de verificación es: {code}",  # Texto alternativo si el cliente no soporta HTML
            from_email=settings.EMAIL_HOST_USER,
            to=[user_mail],  # Pasamos la variable directamente como lista
        )
        email.attach_alternative(content, "text/html")

        # fail_silently= fuerza a que lance excepción si falla el SMTP
        email.send(fail_silently=False)
        return 

    except Exception as e:
        # Captura cualquier error de SMTP, credenciales o caída de red
        log_system_event(
            message=f"Error al enviar correo de verificación a {user_mail}: {e}",
            level_name="ERROR",
            source="send_email_code_verification",
            category_name="Correo"
        )
        return 

# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES



def send_email_user_conect_or_disconect(usuario, hora, estado):
    # 1. Obtener los correos electrónicos de los destinatarios (evitando valores nulos/vacíos)
    try:
        usuarios_email = list(
            User.objects.filter(Q(rol__role_name="Programador"), status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al obtener los correos de los programadores: {e}",
            level_name="ERROR",
            source="Correo",
            category_name="Email",
            traceback=traceback.format_exc(),
            metadata={"usuario_id": getattr(usuario, "id", None)},
        )
        return

    # Si no hay destinatarios o si la bandera SERVIDOR es False, se cancela el envío
    if not SERVIDOR or not usuarios_email:
        if not usuarios_email:
            log_system_event(
                message=f"No se enviará correo para '{usuario}': No hay destinatarios con el rol 'Programador' activos o con correo configurado.",
                level_name="WARNING",
                source="Correo",
                category_name="Email",
            )
        return

    # 2. Intentar renderizar la plantilla HTML
    try:
        template = get_template("email/user_conect.html")
        context = {
            "user": usuario,
            "hora": hora,
            "estado": estado,
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/user_conect.html'.",
            level_name="ERROR",
            source="Correo",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar la plantilla para el correo de estado de conexión: {e}",
            level_name="ERROR",
            source="Correo",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Intentar construir y enviar el correo electrónico
    try:
        email = EmailMultiAlternatives(
            subject=f"USUARIO HA {estado}",
            body=f"El usuario {usuario} ha cambiado su estado a: {estado} a las {hora}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        # Log informativo opcional para confirmar el éxito del envío en la bitácora
        log_system_event(
            message=f"Correo de notificación '{estado}' enviado exitosamente para el usuario {usuario}.",
            level_name="INFO",
            source="Correo",
            category_name="Email",
            metadata={
                "destinatarios": usuarios_email,
                "estado": estado,
                "usuario": str(usuario),
            },
        )

    except Exception as e:
        # Captura cualquier falla SMTP, de credenciales o de red y guarda la trazabilidad completa
        log_system_event(
            message=f"Error al enviar el correo de notificación de estado para {usuario}: {e}",
            level_name="ERROR",
            source="Correo",
            category_name="Email",
            traceback=traceback.format_exc(),
            metadata={"destinatarios": usuarios_email, "estado": estado},
        )
        return

