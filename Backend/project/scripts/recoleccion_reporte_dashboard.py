from apps.financings.models import Credit


def recolectar_informes_status_creditos():
    recoleccion = {
        'creditos':Credit.objects.filter(is_paid_off=False),
        'creditos_atrasados':Credit.objects.filter(estados_fechas=False),
    }

    return recoleccion