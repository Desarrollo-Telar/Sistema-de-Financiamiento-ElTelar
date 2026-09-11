import traceback
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils import timezone

# IMPORTS DEL PROYECTO
from apps.actividades.utils import (
    build_notificacion_especificaciones,
    log_system_event,
    log_user_action,
)
from apps.users.models import User
from project.settings import SERVIDOR
from scripts.notificaciones.creacion_notificacion import (
    creacion_notificacion_administrador_secretaria,
    creacion_notificacion_administradores,
)


# MENSAJE DE CRÉDITO NUEVO
def send_email_new_credit(models):
    # 1. Obtener correos de administradores activos
    try:
        usuarios_email = list(
            User.objects.filter(rol__role_name="Administrador", status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar correos de administradores para crédito nuevo (ID: {getattr(models, 'id', 'Desconocido')}): {e}",
            level_name="ERROR",
            source="Credit Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 2. Validar si procede el envío
    if not SERVIDOR or not usuarios_email:
        if not usuarios_email:
            log_system_event(
                message=f"No se enviará notificación de crédito nuevo ({getattr(models, 'id', '')}): Sin administradores con correo válido.",
                level_name="WARNING",
                source="Credit Service",
                category_name="Email",
            )
        return

    # 3. Renderizar plantilla de correo
    try:
        template = get_template("email/new_credit.html")
        context = {"object_list": models}
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/new_credit.html'.",
            level_name="ERROR",
            source="Credit Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar la plantilla 'email/new_credit.html': {e}",
            level_name="ERROR",
            source="Credit Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 4. Construcción y envío del correo
    try:
        email = EmailMultiAlternatives(
            subject="REGISTRO DE UN NUEVO CRÉDITO",
            body=f"Se ha registrado un nuevo crédito con ID {getattr(models, 'id', '')}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo de crédito nuevo (ID: {getattr(models, 'id', '')}) enviado exitosamente.",
            level_name="INFO",
            source="Credit Service",
            category_name="Email",
            metadata={
                "destinatarios": usuarios_email,
                "credito_id": getattr(models, "id", None),
            },
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de crédito nuevo (ID: {getattr(models, 'id', '')}): {e}",
            level_name="ERROR",
            source="Credit Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )

    # 5. Notificación interna en el sistema
    try:
        sucursal = getattr(models, "sucursal", None)
        especificaciones = build_notificacion_especificaciones(
            view_name="financings:detail_credit", kwargs={"id": models.id}
        )

        mensaje = {
            "title": "Registro de un Crédito Nuevo. 😊",
            "message": "Se ha registrado un nuevo crédito dentro de la plataforma.",
            "especificaciones": especificaciones,
        }
        creacion_notificacion_administradores(mensaje, sucursal)

    except Exception as e:
        log_system_event(
            message=f"Error al crear notificación de crédito nuevo (ID: {getattr(models, 'id', '')}): {e}",
            level_name="ERROR",
            source="Notification Service",
            category_name="Notificaciones",
            traceback=traceback.format_exc(),
        )


# NOTIFICAR CUOTAS EN FECHA DE VENCIMIENTO
def send_email_next_update_of_quotas(cuotas):
    # 1. Obtener correos de programadores activos
    try:
        usuarios_email = list(
            User.objects.filter(rol__role_name="Programador", status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar programadores para alerta de cuotas a vencer: {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    if not SERVIDOR or not usuarios_email:
        return

    # 2. Renderizar plantilla con manejo de fechas seguras
    try:
        hoy = timezone.now()
        dia = hoy.date()
        hasta = hoy + timedelta(days=16)

        template = get_template("email/quotas_defeated.html")
        context = {
            "cuotas": cuotas,
            "full_url": "https://www.ii-eltelarsa.com",
            "actualizacion": hasta.date(),
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/quotas_defeated.html'.",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar plantilla 'email/quotas_defeated.html': {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Envío de correo electrónico
    try:
        email = EmailMultiAlternatives(
            subject=f"Cuotas A Fecha de Vencimiento - {dia}",
            body=f"Reporte de cuotas con fecha de vencimiento al día {dia}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo de cuotas con fecha de vencimiento enviado para el día {dia}.",
            level_name="INFO",
            source="Quota Service",
            category_name="Email",
            metadata={"destinatarios": usuarios_email, "fecha": str(dia)},
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de cuotas con fecha de vencimiento ({dia}): {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )

    # 4. Creación de notificación del sistema
    try:
        especificaciones = build_notificacion_especificaciones(
            view_name="financings:filter_credito_fecha_vencimiento_hoy"
        )
        mensaje = {
            "title": "Cuotas con Fecha Vencimiento Hoy. 😶",
            "message": "Las siguientes cuotas han llegado a su fecha de vencimiento",
            "especificaciones": especificaciones,
        }
        creacion_notificacion_administrador_secretaria(mensaje)
    except Exception as e:
        log_system_event(
            message=f"Error al crear notificación interna para cuotas a vencer ({dia}): {e}",
            level_name="ERROR",
            source="Notification Service",
            category_name="Notificaciones",
            traceback=traceback.format_exc(),
        )


# NOTIFICAR CUOTAS EN FECHA LÍMITE
def send_email_update_of_quotas(cuotas):
    # 1. Obtener correos de programadores activos
    try:
        usuarios_email = list(
            User.objects.filter(rol__role_name="Programador", status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar programadores para cuotas en fecha límite: {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    if not SERVIDOR or not usuarios_email:
        return

    # 2. Renderizar plantilla
    try:
        dia = timezone.now().date()
        template = get_template("email/update_of_quotas.html")
        context = {
            "cuotas": cuotas,
            "full_url": "https://www.ii-eltelarsa.com",
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/update_of_quotas.html'.",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar plantilla 'email/update_of_quotas.html': {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Envío de correo electrónico
    try:
        email = EmailMultiAlternatives(
            subject=f"Actualización de Cuotas Por Fecha Limite - {dia}",
            body=f"Reporte de cuotas que alcanzaron su fecha límite al día {dia}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo de cuotas en fecha límite enviado para el día {dia}.",
            level_name="INFO",
            source="Quota Service",
            category_name="Email",
            metadata={"destinatarios": usuarios_email, "fecha": str(dia)},
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de cuotas en fecha límite ({dia}): {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )

    # 4. Creación de notificación del sistema
    try:
        especificaciones = build_notificacion_especificaciones(
            view_name="financings:filter_credito_fecha_limite_hoy"
        )
        mensaje = {
            "title": "Cuotas con Fecha Limite Hoy. 😵",
            "message": "Las siguientes cuotas han llegado a su fecha límite",
            "especificaciones": especificaciones,
        }
        creacion_notificacion_administrador_secretaria(mensaje)
    except Exception as e:
        log_system_event(
            message=f"Error al crear notificación de cuotas en fecha límite ({dia}): {e}",
            level_name="ERROR",
            source="Notification Service",
            category_name="Notificaciones",
            traceback=traceback.format_exc(),
        )


# NOTIFICAR CUOTAS PRÓXIMAS A CAMBIAR DE ESTADO
def send_email_quotas_for_change(cuotas, hoy, hasta):
    # 1. Obtener correos de programadores activos
    try:
        usuarios_email = list(
            User.objects.filter(rol__role_name="Programador", status=True)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar programadores para cuotas próximas a cambiar: {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    if not SERVIDOR or not usuarios_email:
        return

    # 2. Renderizar plantilla
    try:
        dia = timezone.now().date()
        template = get_template("email/quotas_for_change.html")
        context = {
            "cuotas": cuotas,
            "full_url": "https://www.ii-eltelarsa.com",
            "hoy": hoy,
            "hasta": hasta,
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/quotas_for_change.html'.",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar la plantilla 'email/quotas_for_change.html': {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Envío de correo electrónico
    try:
        email = EmailMultiAlternatives(
            subject=f"Próximas Cuotas En Llegar a su Fecha de Vencimiento, TOMAR NOTA - {dia}",
            body=f"Reporte de próximas cuotas por vencer entre {hoy} y {hasta}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo de cuotas próximas a vencer ({hoy} a {hasta}) enviado exitosamente.",
            level_name="INFO",
            source="Quota Service",
            category_name="Email",
            metadata={
                "destinatarios": usuarios_email,
                "rango": f"{hoy} - {hasta}",
            },
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de cuotas próximas a vencer ({hoy} a {hasta}): {e}",
            level_name="ERROR",
            source="Quota Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )