import traceback
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

# IMPORTS DEL PROYECTO
from apps.actividades.utils import (
    build_notificacion_especificaciones,
    log_system_event,
    log_user_action,
)
from apps.users.models import User
from project.settings import SERVIDOR
from scripts.notificaciones.creacion_notificacion import (
    creacion_notificacion_administradores,
)


# ENVIO DE MENSAJE DE EMAIL PARA DARLE LA BIENVENIDA A UN CLIENTE
def send_email_welcome_customer(customer):
    customer_email = getattr(customer, "email", None)

    # 1. Validar que el cliente tenga un correo válido
    if not customer_email:
        log_system_event(
            message=f"No se envió correo de bienvenida: El cliente '{getattr(customer, 'id', 'Desconocido')}' no tiene email configurado.",
            level_name="WARNING",
            source="Customer Service",
            category_name="Email",
        )
        return

    # 2. Renderizar plantilla de correo
    try:
        template = get_template("email/welcome_message.html")
        context = {
            "nombre_usuario": customer.get_full_name(),
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/welcome_message.html'.",
            level_name="ERROR",
            source="Customer Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar plantilla de bienvenida para cliente {customer_email}: {e}",
            level_name="ERROR",
            source="Customer Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Construir y enviar el correo si SERVIDOR es True
    if SERVIDOR:
        try:
            email = EmailMultiAlternatives(
                subject="BIENVENIDO",
                body=f"Bienvenido/a {customer.get_full_name()} a ELTELAR.",
                from_email=settings.EMAIL_HOST_USER,
                to=[customer_email],
            )
            email.attach_alternative(content, "text/html")
            email.send(fail_silently=False)

            log_system_event(
                message=f"Correo de bienvenida enviado exitosamente al cliente {customer_email}.",
                level_name="INFO",
                source="Customer Service",
                category_name="Email",
                metadata={"customer_id": getattr(customer, "id", None)},
            )
        except Exception as e:
            log_system_event(
                message=f"Error al enviar correo de bienvenida al cliente {customer_email}: {e}",
                level_name="ERROR",
                source="Customer Service",
                category_name="Email",
                traceback=traceback.format_exc(),
            )


# NOTIFICAR A TODOS LOS ADMINISTRADORES DE UN NUEVO CLIENTE EN LA EMPRESA
def send_email_new_customer(customer):
    # 1. Obtener correos de administradores activos evitando vacíos/nulos
    try:
        usuarios_email = list(
            User.objects.filter(rol__role_name="Administrador", status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar correos de administradores para notificación de cliente nuevo: {e}",
            level_name="ERROR",
            source="Customer Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 2. Validar si procede el envío
    if not SERVIDOR or not usuarios_email:
        if not usuarios_email:
            log_system_event(
                message=f"No se enviará notificación de cliente nuevo ({getattr(customer, 'customer_code', '')}): No hay administradores activos con email.",
                level_name="WARNING",
                source="Customer Service",
                category_name="Email",
            )
        return

    # 3. Renderizar plantilla de correo
    try:
        template = get_template("email/message_new_customer.html")
        context = {
            "nombre_usuario": customer.get_full_name(),
            "email": getattr(customer, "email", ""),
            "date": getattr(customer, "creation_date", ""),
            "code": getattr(customer, "customer_code", ""),
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/message_new_customer.html'.",
            level_name="ERROR",
            source="Customer Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar plantilla 'email/message_new_customer.html': {e}",
            level_name="ERROR",
            source="Customer Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 4. Construcción y envío del correo a administradores
    try:
        customer_code = getattr(customer, "customer_code", "")
        email = EmailMultiAlternatives(
            subject="CLIENTE NUEVO",
            body=f"Se ha registrado un nuevo cliente: {customer.get_full_name()} (Código: {customer_code}).",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo de alerta por nuevo cliente ({customer_code}) enviado a administradores.",
            level_name="INFO",
            source="Customer Service",
            category_name="Email",
            metadata={
                "destinatarios": usuarios_email,
                "customer_code": customer_code,
            },
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de cliente nuevo para {getattr(customer, 'customer_code', '')}: {e}",
            level_name="ERROR",
            source="Customer Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )

    # 5. Generación de notificación interna en el sistema
    try:
        especificaciones = build_notificacion_especificaciones(
            view_name="customers:detail",
            kwargs={"customer_code": customer.customer_code},
            extra_data={
                "contenido": f"\nDetalles del Cliente:\nNombre: {customer.first_name}\nCorreo Electronico: {customer.email}\nCodigo del Cliente: {customer.customer_code}\n"
            },
        )

        mensaje = {
            "title": "Registro de Cliente Nuevo. 😏",
            "message": "Se ha registrado un cliente nuevo",
            "especificaciones": especificaciones,
        }
        creacion_notificacion_administradores(mensaje)

    except Exception as e:
        log_system_event(
            message=f"Error al crear notificación interna para cliente nuevo ({getattr(customer, 'customer_code', '')}): {e}",
            level_name="ERROR",
            source="Notification Service",
            category_name="Notificaciones",
            traceback=traceback.format_exc(),
        )