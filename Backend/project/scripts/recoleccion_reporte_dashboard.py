from apps.financings.models import Credit
from apps.customers.models import CreditCounselor


def recolectar_informes_status_creditos(request):
    creditos = Credit.objects.filter(is_paid_off=False)
    creditos_atrasados = Credit.objects.filter(estados_fechas=False)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        creditos = Credit.objects.filter(is_paid_off=False, customer_id__new_asesor_credito=asesor_autenticado)
        creditos_atrasados = Credit.objects.filter(estados_fechas=False, customer_id__new_asesor_credito=asesor_autenticado)

    recoleccion = {
        'creditos':creditos,
        'creditos_atrasados':creditos_atrasados,
    }

    return recoleccion