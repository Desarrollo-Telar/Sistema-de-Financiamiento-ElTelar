# Models
from apps.customers.models import Customer
from apps.financings.models import Credit
from apps.actividades.models import Informe, DetalleInformeCobranza


def recoleccion_informacion_detalle_asesor(asesor):

    contexto = {
        'clientes':Customer.objects.filter(new_asesor_credito__id = asesor.id),
        'creditos':Credit.objects.filter(customer_id__new_asesor_credito__id = asesor.id).order_by('-creation_date'),
        'creditos_vigentes':Credit.objects.filter(customer_id__new_asesor_credito__id = asesor.id, is_paid_off = False ).order_by('-creation_date'),
        'creditos_atrasados_por_fecha':Credit.objects.filter(customer_id__new_asesor_credito__id = asesor.id, estados_fechas = False ).order_by('-creation_date'),
        'creditos_atrasados_por_aportacion':Credit.objects.filter(customer_id__new_asesor_credito__id = asesor.id, estado_aportacion = False ).order_by('-creation_date'),
        'reportes':  Informe.objects.filter(usuario__id = asesor.usuario.id).order_by('-id'),
        'usuario': asesor.usuario,
    }
    return contexto