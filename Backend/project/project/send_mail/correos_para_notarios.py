from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

from apps.users.models import User

from project.settings import SERVIDOR

# CONSULTAS
from django.db.models import Q

from apps.InvestmentPlan.models import InvestmentPlan


# Asegúrate de importar tu modelo InvestmentPlan

def send_email_notario(user, plan_inversion_id, formato='formato_01'):
    # 1. Obtenemos el plan de inversión
    plan_inversion = InvestmentPlan.objects.get(id=plan_inversion_id)
    
    # 2. Extraemos la lista completa de garantías del JSONField
    # Usamos .garantias o el nombre exacto del campo en tu modelo InvestmentPlan
    garantias_totales = plan_inversion.garantias or []
    
    # 3. Filtramos las garantías que pertenecen a este notario específico
    id_notario = user.id
   

    # 2. Filtramos aplicando las exclusiones solicitadas
    garantias_filtradas = []
    for g in garantias_totales:
        tipo = g.get('tipo')
        notario_data = g.get('notario')  # Puede ser un diccionario o None
        
        if tipo == 'CHEQUE / PAGARE':
            if notario_data:
                # Si tiene notario, SOLO pasa si coincide con el notario actual
                if notario_data.get('id') == id_notario:
                    garantias_filtradas.append(g)
            else:
                # Si es un cheque/pagaré pero NO tiene notario vinculado, SÍ se muestra
                garantias_filtradas.append(g)
        else:
            # Cualquier otro tipo de garantía (Hipoteca, etc.) SIEMPRE se muestra
            garantias_filtradas.append(g)

    # 3. Si la lista resultante quedó vacía, la pasamos como None
    garantias_contexto = garantias_filtradas if garantias_filtradas else None
    
  

    # 5. Preparación del correo
    template = get_template(f'email/notario/{formato}.html')
    user_mail = user.email


    if formato == 'formato_01':
        asunto = f"Solicitud de Instrumento Público y Formalización de Garantías – [ {plan_inversion.customer_id}] – Oficina [ {plan_inversion.sucursal} ]"
    

    if formato == 'formato_02':
        asunto = f"Solicitud de Elaboración de {plan_inversion.tipo_documento} – [ {plan_inversion.customer_id}] – Oficina [ {plan_inversion.sucursal} ]"
    
    if formato == 'formato_03':
        asunto = f"Solicitud de Elaboración de Garantías (Cheque/Pagaré) – [ {plan_inversion.customer_id}] – Oficina [ {plan_inversion.sucursal} ]"

    accion = f"Se le notifica que tiene garantias asignadas en el Plan de Inversión {plan_inversion.id}."

    context = {
        'user': user,
        'plan_inversion': plan_inversion,
        'garantias': garantias_contexto,  # Aquí pasamos las garantías filtradas o None
        'accion': accion,
        'direccion': plan_inversion.customer_id.get_direccion(),
        'tipo_documento': plan_inversion.tipo_documento, 
        
    }

    content = template.render(context)
 
    email = EmailMultiAlternatives(
        f'{asunto}',
        'IIELTELAR',
        settings.EMAIL_HOST_USER,
        [user_mail]
    )
    email.attach_alternative(content, 'text/html')
    
    email.send()