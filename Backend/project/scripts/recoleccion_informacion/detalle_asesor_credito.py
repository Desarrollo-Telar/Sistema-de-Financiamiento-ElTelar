# Models
from apps.customers.models import Customer
from apps.financings.models import Credit

def recoleccion_informacion_detalle_asesor(asesor):
    contexto = {
        'clientes':Customer.objects.filter(new_asesor_credito__id = asesor.id),
        'creditos':Credit.objects.filter(customer_id__new_asesor_credito__id = asesor.id).order_by('-creation_date')

    }
    return contexto