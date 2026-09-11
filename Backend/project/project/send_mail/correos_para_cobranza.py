import traceback
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

# IMPORTS DEL PROYECTO
from apps.actividades.models import DetalleInformeCobranza
from apps.actividades.utils import (
    build_notificacion_especificaciones,
    log_system_event,
    log_user_action,
)
from apps.users.models import User
from project.settings import SERVIDOR
from scripts.notificaciones.creacion_notificacion import creacion_notificacion


# MENSAJES DE ALERTAS PARA LOS ADMINISTRADORES
def send_email_recordatorio_cobranza(models):
    # 1. Obtener el asesor de crédito y sus datos con seguridad
    asesor_credito = getattr(models, "asesor_credito", None)
    asesor_user_id = (
        getattr(asesor_credito.usuario, "id", None)
        if (asesor_credito and hasattr(asesor_credito, "usuario"))
        else None
    )

    # 2. Consultar destinatarios (Administradores, Programadores y el Asesor específico)
    roles = ["Administrador", "Programador"]

    try:
        query_destinatarios = Q(rol__role_name__in=roles) & Q(status=True)
        if asesor_user_id:
            query_destinatarios |= Q(id=asesor_user_id)

        usuarios_email = list(
            User.objects.filter(query_destinatarios)
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
            .distinct()
        )
    except Exception as e:
        log_system_event(
            message=f"Error al consultar usuarios para recordatorio de cobranza (Cobranza ID: {getattr(models, 'id', 'Desconocido')}): {e}",
            level_name="ERROR",
            source="Cobranza Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 3. Validar si procede el envío
    if not SERVIDOR or not usuarios_email:
        if not usuarios_email:
            log_system_event(
                message=f"No se enviará recordatorio de cobranza ({getattr(models, 'id', '')}): Sin correos válidos para roles {roles} o el asesor.",
                level_name="WARNING",
                source="Cobranza Service",
                category_name="Email",
            )
        return

    # 4. Obtener detalle de cobranza y renderizar plantilla HTML
    try:
        detalle_informe = DetalleInformeCobranza.objects.filter(
            cobranza__id=models.id
        ).first()
        full_url = "https://www.ii-eltelarsa.com"

        template = get_template("email/recordatorio_cobranza.html")
        context = {
            "full_url": full_url,
            "object": models,
            "detalle_informe": detalle_informe,
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message="No se encontró la plantilla 'email/recordatorio_cobranza.html'.",
            level_name="ERROR",
            source="Cobranza Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar plantilla de recordatorio de cobranza: {e}",
            level_name="ERROR",
            source="Cobranza Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 5. Construir y enviar el correo electrónico
    try:
        credito_info = getattr(models, "credito", "N/A")
        email = EmailMultiAlternatives(
            subject=f"Recordatorio para la gestion de cobranza de: {credito_info}",
            body=f"Recordatorio de gestión de cobranza para el crédito {credito_info}.",
            from_email=settings.EMAIL_HOST_USER,
            to=usuarios_email,
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo de recordatorio de cobranza enviado para el crédito {credito_info}.",
            level_name="INFO",
            source="Cobranza Service",
            category_name="Email",
            metadata={
                "destinatarios": usuarios_email,
                "cobranza_id": getattr(models, "id", None),
                "credito": str(credito_info),
            },
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de recordatorio de cobranza para {getattr(models, 'credito', '')}: {e}",
            level_name="ERROR",
            source="Cobranza Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return