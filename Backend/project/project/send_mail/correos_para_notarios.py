import traceback
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from apps.actividades.utils import log_system_event
from apps.InvestmentPlan.models import InvestmentPlan
from project.settings import SERVIDOR


def send_email_notario(user, plan_inversion_id, formato="formato_01", uuid=None):
    # 1. Obtención segura del plan de inversión
    try:
        plan_inversion = InvestmentPlan.objects.get(id=plan_inversion_id)
    except InvestmentPlan.DoesNotExist:
        log_system_event(
            message=f"No se encontró el Plan de Inversión con ID {plan_inversion_id} para enviar correo al notario.",
            level_name="ERROR",
            source="Notary Email Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error inesperado al obtener el Plan de Inversión ID {plan_inversion_id}: {e}",
            level_name="ERROR",
            source="Notary Email Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 2. Validar que el usuario notario tenga un correo electrónico configurado
    user_mail = getattr(user, "email", None)
    if not user_mail:
        log_system_event(
            message=f"El notario {getattr(user, 'username', 'Desconocido')} (ID: {getattr(user, 'id', None)}) no posee una dirección de correo válida.",
            level_name="WARNING",
            source="Notary Email Service",
            category_name="Email",
        )
        return

    # 3. Filtrado de garantías según lógica de notario asignado
    garantias_totales = plan_inversion.garantias or []
    id_notario = user.id
    garantias_filtradas = []

    for g in garantias_totales:
        if not isinstance(g, dict):
            continue

        tipo = g.get("tipo")
        notario_data = g.get("notario")  # Puede ser un dict o None

        if tipo == "CHEQUE / PAGARE":
            if notario_data and isinstance(notario_data, dict):
                # Si tiene notario asignado, solo pasa si coincide el ID
                if notario_data.get("id") == id_notario:
                    garantias_filtradas.append(g)
            else:
                # Si no tiene notario vinculado, se incluye
                garantias_filtradas.append(g)
        else:
            # Cualquier otro tipo de garantía (Hipoteca, etc.) pasa directo
            garantias_filtradas.append(g)

    garantias_contexto = garantias_filtradas if garantias_filtradas else None

    # 4. Asignación dinámica del asunto según el formato
    cliente_str = getattr(plan_inversion, "customer_id", "")
    sucursal_str = getattr(plan_inversion, "sucursal", "")
    tipo_doc_str = getattr(plan_inversion, "tipo_documento", "Documento")

    asunto_map = {
        "formato_01": f"Solicitud de Instrumento Público y Formalización de Garantías – [ {cliente_str} ] – Oficina [ {sucursal_str} ]",
        "formato_02": f"Solicitud de Elaboración de {tipo_doc_str} – [ {cliente_str} ] – Oficina [ {sucursal_str} ]",
        "formato_03": f"Solicitud de Elaboración de Garantías (Cheque/Pagaré) – [ {cliente_str} ] – Oficina [ {sucursal_str} ]",
    }
    asunto = asunto_map.get(
        formato,
        f"Solicitud de Notaría – [ {cliente_str} ] – Oficina [ {sucursal_str} ]",
    )

    # 5. Obtención segura de dirección del cliente
    customer_obj = getattr(plan_inversion, "customer_id", None)
    direccion = ""
    if customer_obj and hasattr(customer_obj, "get_direccion"):
        try:
            direccion = customer_obj.get_direccion()
        except Exception:
            direccion = ""

    # 6. Renderizado de la plantilla HTML
    template_path = f"email/notario/{formato}.html"
    try:
        template = get_template(template_path)
        context = {
            "user": user,
            "plan_inversion": plan_inversion,
            "garantias": garantias_contexto,
            "accion": f"Se le notifica que tiene garantías asignadas en el Plan de Inversión {plan_inversion.id}.",
            "direccion": direccion,
            "tipo_documento": tipo_doc_str,
            "uuid": uuid,
        }
        content = template.render(context)
    except TemplateDoesNotExist:
        log_system_event(
            message=f"No se encontró la plantilla de correo en la ruta '{template_path}'.",
            level_name="ERROR",
            source="Notary Email Service",
            category_name="Email",
        )
        return
    except Exception as e:
        log_system_event(
            message=f"Error al renderizar plantilla '{template_path}' para el notario {user_mail}: {e}",
            level_name="ERROR",
            source="Notary Email Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )
        return

    # 7. Envío del correo electrónico si está habilitado el servidor
    if not SERVIDOR:
        log_system_event(
            message=f"Envío de correo a notario simulado (SERVIDOR=False). Destinatario: {user_mail}, Plan ID: {plan_inversion.id}",
            level_name="INFO",
            source="Notary Email Service",
            category_name="Email",
        )
        return

    try:
        email = EmailMultiAlternatives(
            subject=asunto,
            body=f"Notificación de asignación de garantías en Plan de Inversión ID: {plan_inversion.id}",
            from_email=settings.EMAIL_HOST_USER,
            to=[user_mail],
        )
        email.attach_alternative(content, "text/html")
        email.send(fail_silently=False)

        log_system_event(
            message=f"Correo enviado exitosamente al notario {user_mail} para el Plan de Inversión ID {plan_inversion.id}.",
            level_name="INFO",
            source="Notary Email Service",
            category_name="Email",
            metadata={
                "notario_id": user.id,
                "plan_inversion_id": plan_inversion.id,
                "formato": formato,
                "uuid": str(uuid) if uuid else None,
            },
        )
    except Exception as e:
        log_system_event(
            message=f"Error al enviar correo de notario a {user_mail} (Plan ID: {plan_inversion.id}): {e}",
            level_name="ERROR",
            source="Notary Email Service",
            category_name="Email",
            traceback=traceback.format_exc(),
        )