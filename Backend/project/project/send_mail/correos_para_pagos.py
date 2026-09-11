import traceback
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

# MODELOS E IMPORTS DE TU PROYECTO
from apps.actividades.utils import (
    build_notificacion_especificaciones,
    log_system_event,
    log_user_action,
)
from apps.users.models import User
from project.settings import SERVIDOR
from scripts.notificaciones.creacion_notificacion import creacion_notificacion


# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
def send_email_alert(message, status, models):
    # 1. Verificación inicial de registro ficticio
    if getattr(models, "registro_ficticio", False):
        return

    # 2. Definición de roles y obtención de destinatarios
    roles = ["Administrador", "Programador"]
    lista_tipos = ["DESEMBOLSO", "CREDITO"]

    if getattr(models, "tipo_pago", None) in lista_tipos:
        roles.append("Secretari@")

    try:
        usuarios_email = list(
            User.objects.filter(rol__role_name__in=roles, status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar destinatarios para alerta de boleta {getattr(models, 'numero_referencia', '')}: {e}",
            level_name="ERROR",
            source="Alert Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Validar si procede el envío
    if not SERVIDOR or not usuarios_email:
        if not usuarios_email:
            log_system_event(
                message=f"No se enviará alerta de boleta ({getattr(models, 'numero_referencia', '')}): Sin correos válidos para los roles {roles}.",
                level_name="WARNING",
                source="Alert Service",
                category_name="Email",
            )
        return

    # 4. Renderizar plantilla de correo
    try:
        template = get_template("email/alert_message.html")
        full_url = "https://www.ii-eltelarsa.com"
        context = {
            "message": message,
            "full_url": full_url,
            "object": models,
            "status": status,
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/alert_message.html'.",
            level_name="ERROR",
            source="Alert Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar plantilla 'email/alert_message.html': {e}",
            level_name="ERROR",
            source="Alert Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 5. Construcción y envío del correo electrónico
    try:
        email = EmailMultiAlternatives(
            subject=f"ALERTA {status} PARA {models.numero_referencia}",
            body=f"Alerta {status} para la boleta {models.numero_referencia}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")

        # Descomenta email.send() para producción
        # email.send(fail_silently=False)

        log_system_event(
            message=f"Alerta de correo procesada para la boleta {models.numero_referencia} ({status}).",
            level_name="INFO",
            source="Alert Service",
            category_name="Email",
            metadata={
                "destinatarios": usuarios_email,
                "referencia": getattr(models, "numero_referencia", None),
            },
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de alerta para {models.numero_referencia}: {e}",
            level_name="ERROR",
            source="Alert Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )

    # 6. Creación de notificación en el sistema
    try:
        sucursal = getattr(models, "sucursal", None)
        especificaciones = build_notificacion_especificaciones(
            view_name="financings:detalle_boleta",
            kwargs={"id": models.id},
            extra_data={
                "contenido": f"\nNumero de Referencia: {models.numero_referencia}\nMonto: Q {models.Fmonto()}\nPara: {models.boleta_para()}\n"
            },
        )

        emojin = "😎" if status == "COMPLETADO" else "😕"

        mensaje_notif = {
            "title": f"ALERTA DE BOLETA. {emojin}",
            "message": f"La siguiente boleta con {models.numero_referencia} esta en status {status}",
            "especificaciones": especificaciones,
        }
        creacion_notificacion(roles, mensaje_notif, sucursal)

    except Exception as e:
        log_system_event(
            message=f"Error al crear notificación interna para boleta {getattr(models, 'numero_referencia', '')}: {e}",
            level_name="ERROR",
            source="Notification Service",
            category_name="Notificaciones",
            traceback=traceback.format_exc(),
        )


# MENSAJES PARA EL MANEJO DE RECIBOS
def send_email_recibo(models):
    # 1. Verificación inicial de registro ficticio en el pago asociado
    if getattr(models.pago, "registro_ficticio", False):
        return

    # 2. Definición de roles y obtención de destinatarios
    roles = ["Administrador", "Programador"]
    lista_tipos = ["DESEMBOLSO", "CREDITO"]

    if getattr(models.pago, "tipo_pago", None) in lista_tipos:
        roles.append("Secretari@")

    try:
        usuarios_email = list(
            User.objects.filter(rol__role_name__in=roles, status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar destinatarios para recibo de {getattr(models.pago, 'id', 'desconocido')}: {e}",
            level_name="ERROR",
            source="Recibo Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Validar si procede el envío
    if not SERVIDOR or not usuarios_email:
        if not usuarios_email:
            log_system_event(
                message=f"No se enviará recibo de pago {models.pago.id}: No hay usuarios con email activo en roles {roles}.",
                level_name="WARNING",
                source="Recibo Service",
                category_name="Email",
            )
        return

    # 4. Renderizar plantilla de correo
    try:
        template = get_template("email/recibo.html")
        context = {"recibo": models}
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/recibo.html'.",
            level_name="ERROR",
            source="Recibo Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar la plantilla 'email/recibo.html': {e}",
            level_name="ERROR",
            source="Recibo Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 5. Construcción y envío del correo electrónico
    try:
        boleta_para = models.pago.boleta_para()
        email = EmailMultiAlternatives(
            subject=f"RECIBO DE {boleta_para}",
            body=f"Se ha generado un recibo para {boleta_para}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo de recibo enviado exitosamente para {boleta_para}.",
            level_name="INFO",
            source="Recibo Service",
            category_name="Email",
            metadata={
                "destinatarios": usuarios_email,
                "pago_id": models.pago.id,
            },
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de recibo para el pago {models.pago.id}: {e}",
            level_name="ERROR",
            source="Recibo Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )

    # 6. Creación de notificación en el sistema
    try:
        sucursal = getattr(models, "sucursal", None)
        especificaciones = build_notificacion_especificaciones(
            view_name="financings:recibo", kwargs={"id": models.pago.id}
        )

        mensaje_notif = {
            "title": "Se creo un Recibo. 📋",
            "message": f"Recibo para {models.pago.boleta_para()}",
            "especificaciones": especificaciones,
        }
        creacion_notificacion(roles, mensaje_notif, sucursal)

    except Exception as e:
        log_system_event(
            message=f"Error al crear notificación de recibo para el pago {models.pago.id}: {e}",
            level_name="ERROR",
            source="Notification Service",
            category_name="Notificaciones",
            traceback=traceback.format_exc(),
        )