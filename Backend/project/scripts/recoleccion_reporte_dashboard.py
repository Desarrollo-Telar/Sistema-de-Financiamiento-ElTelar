# Modelos
from apps.financings.models import Credit, PaymentPlan
from apps.customers.models import CreditCounselor, Cobranza
from apps.actividades.models import DetalleInformeCobranza, Informe

# Tiempo
from datetime import datetime, timedelta

from apps.financings.formato import formatear_numero

def cuota(creditos):
   dia = datetime.now().date()
   dia_mas_uno = dia + timedelta(days=1)
   cuota_actual = None
   saldo_capital = 0
   informacion_actual = {}

   for credito in creditos:
      cuota_actual = PaymentPlan.objects.filter(
         credit_id=credito,
         start_date__lte=dia,
         fecha_limite__gte=dia_mas_uno
      ).first()

      if cuota_actual is not None:
        saldo_capital += cuota_actual.saldo_pendiente


   informacion_actual['saldo_capital'] = saldo_capital
    
   

   return saldo_capital 

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
    sucursal = request.session['sucursal_id']
    dia = datetime.now().date()
    hoy = datetime.now()
    hasta = hoy + timedelta(days=7)

    # Base filters comunes
    base_credit_filter = {"sucursal": sucursal, "is_paid_off": False}
    base_plan_filter = {"sucursal": sucursal, "credit_id__estado_judicial" : False, "credit_id__is_paid_off" : False}

    # Si el usuario es asesor, filtramos además por su registro
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
    if asesor_autenticado and request.user.rol.role_name == 'Asesor de Crédito':
        base_credit_filter["asesor_de_credito"] = asesor_autenticado
        base_plan_filter["credit_id__asesor_de_credito"] = asesor_autenticado

    # Si el usuario es secretari@, filtramos por créditos válidos
    if request.user.rol.role_name == 'Secretari@':
        base_plan_filter["credit_id__isnull"] = False

    # Consultas principales
    creditos = Credit.objects.filter(**base_credit_filter).exclude(estado_judicial=True)
    creditos_atrasados = Credit.objects.filter(estados_fechas=False, **base_credit_filter).exclude(estado_judicial=True)

    saldo_actual_todos = cuota(creditos)
    saldo_acutal_atrasados =  cuota(creditos_atrasados)

    indicador_mora = 0

    creditos_fecha_limite = PaymentPlan.objects.filter(
        fecha_limite__date=dia, **base_plan_filter
    )
    creditos_fecha_vencimiento = PaymentPlan.objects.filter(
        due_date__date=dia, **base_plan_filter
    )
    creditos_proximos_vencerse = PaymentPlan.objects.filter(
        due_date__range=[hoy, hasta],
        status=False,
        **base_plan_filter
    ).order_by("due_date")


    recoleccion = {
        'creditos':creditos,
        'creditos_atrasados':creditos_atrasados,
        'creditos_fecha_vencimiento':creditos_fecha_vencimiento,
        'creditos_fecha_limite':creditos_fecha_limite,
        'creditos_proximos_vencerse':creditos_proximos_vencerse,
        'saldo_actual_todos': formatear_numero(saldo_actual_todos),
        'saldo_acutal_atrasados': formatear_numero(saldo_acutal_atrasados),
        'indicador_mora':indicador_mora
    }

    return recoleccion