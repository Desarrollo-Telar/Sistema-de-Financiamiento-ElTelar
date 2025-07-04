# Modelos
from apps.financings.models import Credit, PaymentPlan
from apps.customers.models import CreditCounselor

# Tiempo
from datetime import datetime

def recolectar_informes_status_creditos(request):
    dia = datetime.now().date() # Obtener el dia 

    creditos = Credit.objects.filter(is_paid_off=False)
    creditos_atrasados = Credit.objects.filter(estados_fechas=False)
    creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia)

    creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia)

    

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos = Credit.objects.filter(is_paid_off=False, customer_id__new_asesor_credito=asesor_autenticado)
        creditos_atrasados = Credit.objects.filter(estados_fechas=False, customer_id__new_asesor_credito=asesor_autenticado)

        creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia, credit_id__customer_id__new_asesor_credito=asesor_autenticado)
        creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia,  credit_id__customer_id__new_asesor_credito=asesor_autenticado)

    recoleccion = {
        'creditos':creditos,
        'creditos_atrasados':creditos_atrasados,
        'creditos_fecha_vencimiento':creditos_fecha_vencimiento,
        'creditos_fecha_limite':creditos_fecha_limite,
    }

    return recoleccion