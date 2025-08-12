# Modelos
from apps.financings.models import Credit, PaymentPlan
from apps.customers.models import CreditCounselor, Cobranza
from apps.actividades.models import DetalleInformeCobranza, Informe

# Tiempo
from datetime import datetime, timedelta

def recolectar_informacion_cobranza(asesor_autenticado):
    if asesor_autenticado is None:
        return None
    
    informe_vigente = Informe.objects.filter(usuario= asesor_autenticado.usuario, esta_activo=True).first()

    if informe_vigente is None:
        return None
    
    detalle_informe_cobranza = DetalleInformeCobranza.objects.filter(reporte=informe_vigente).order_by('-id')
    cobranza = detalle_informe_cobranza[:10]
    pendientes = detalle_informe_cobranza.filter(cobranza__estado_cobranza = 'Pendiente')
    completados = detalle_informe_cobranza.filter(cobranza__estado_cobranza = 'COMPLETADO')

    recolecion = {
        'ultimos_10': cobranza,
        'pendientes': pendientes.count(),
        'completados':completados.count(),
        'total':detalle_informe_cobranza.count()

    }
    return recolecion


def recolectar_informes_status_creditos(request):
    dia = datetime.now().date() # Obtener el dia 

    creditos = Credit.objects.filter(is_paid_off=False)
    creditos_atrasados = Credit.objects.filter(estados_fechas=False)
    creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia)

    creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia)

    hoy = datetime.now() 
    hasta = hoy + timedelta(days=7)

    creditos_proximos_vencerse= PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False).order_by('due_date')

    

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos = Credit.objects.filter(is_paid_off=False, customer_id__new_asesor_credito=asesor_autenticado)
        creditos_atrasados = Credit.objects.filter(estados_fechas=False, customer_id__new_asesor_credito=asesor_autenticado)

        creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia, credit_id__customer_id__new_asesor_credito=asesor_autenticado)
        creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia,  credit_id__customer_id__new_asesor_credito=asesor_autenticado)
        creditos_proximos_vencerse= PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False, credit_id__customer_id__new_asesor_credito=asesor_autenticado).order_by('due_date')
    
    if request.user.rol.role_name == 'Secretari@':
        creditos_fecha_limite = PaymentPlan.objects.filter(fecha_limite__date=dia, credit_id__isnull=False)
        creditos_fecha_vencimiento = PaymentPlan.objects.filter(due_date__date=dia, credit_id__isnull=False)
        creditos_proximos_vencerse= PaymentPlan.objects.filter(due_date__range=[hoy, hasta], status=False, credit_id__isnull=False).order_by('due_date')


    recoleccion = {
        'creditos':creditos,
        'creditos_atrasados':creditos_atrasados,
        'creditos_fecha_vencimiento':creditos_fecha_vencimiento,
        'creditos_fecha_limite':creditos_fecha_limite,
        'creditos_proximos_vencerse':creditos_proximos_vencerse,
    }

    return recoleccion