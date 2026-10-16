
from django.db.models import Q
from apps.financings.models import AccountStatement

def obtencion_credito_en_pago(instance):
    """
    Identifica la entidad afectada por el pago y procede a corregir sus saldos.
    """
    if instance.credit is not None:
        corregir_credito(instance.credit, 'CREDITO', instance)
        return instance.credit

    if instance.acreedor is not None:
        corregir_credito(instance.acreedor, 'ACREEDOR', instance)
        return instance.acreedor

    if instance.seguro is not None:
        corregir_credito(instance.seguro, 'SEGUROS', instance)
        return instance.seguro

    return None


def corregir_credito(entidad, tipo, pago_actual):
    """
    Restaura los valores de la entidad basándose en el estado de cuenta anterior.
    """
    excedente = getattr(entidad, 'excedente', 0)

    filtros = Q(description='PAGO DE CREDITO')

    if tipo == 'CREDITO':
        filtros &= Q(credit=entidad)
    elif tipo == 'ACREEDOR':
        filtros &= Q(acreedor=entidad)
    elif tipo == 'SEGUROS':
        filtros &= Q(seguro=entidad)

    
    estado_cuenta = AccountStatement.objects.filter(filtros).exclude(payment=pago_actual).order_by('-id').first()
    
    saldos = estado_cuenta.saldo_pendiente if estado_cuenta else 0

    if getattr(entidad, 'is_paid_off', False):
        entidad.is_paid_off = False

    if excedente > 0:
        entidad.excedente = 0

    if entidad.saldo_pendiente > saldos:
        entidad.saldo_pendiente = saldos

    entidad.save()


