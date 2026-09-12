# Tiempo
from datetime import datetime,timedelta

from apps.financings.models import PaymentPlan

from django.db.models import Q


def obtener_cuota_vigente(objeto, fecha_emision=None):
    """
    Obtiene la cuota correspondiente para un Crédito, Acreedor o Seguro.
    Permite evaluar fechas históricas y evita múltiples consultas ORM.
    """
    if fecha_emision is None:
        fecha_emision = datetime.now().date()
    elif isinstance(fecha_emision, datetime):
        fecha_emision = fecha_emision.date()

    # Identificar el tipo de objeto para aplicar el filtro dinámico
    filtro_relacion = {}
    if hasattr(objeto, 'is_paid_off'):  # Es un Crédito
        filtro_relacion = {'credit_id': objeto}
        # Si el crédito está cancelado, traemos la última cuota registrada
        if objeto.is_paid_off:
            return PaymentPlan.objects.filter(**filtro_relacion).order_by('-id').first()

    elif hasattr(objeto, 'acreedor'):   # Es un objeto Creditor o similar
        filtro_relacion = {'acreedor': objeto}
    elif hasattr(objeto, 'seguro'):     # Es un objeto Insurance o similar
        filtro_relacion = {'seguro': objeto}
    else:
        # Si se pasa la relación directa en un kwargs/diccionario
        filtro_relacion = objeto

    # Buscar la cuota dentro del rango de la fecha especificada
    # Usamos lt para replicar la lógica de excluir la fecha_limite exacta si es necesario
    cuota_actual = PaymentPlan.objects.filter(
        start_date__date__lte=fecha_emision,
        fecha_limite__date__gt=fecha_emision,
        **filtro_relacion
    ).first()

    # Fallback: Si no se encuentra una cuota activa en el rango, obtiene la más reciente
    if not cuota_actual:
        cuota_actual = PaymentPlan.objects.filter(**filtro_relacion).order_by('-id').first()

    return cuota_actual

def cuota(credito):
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    cuota_actual = None

    if credito.is_paid_off:
        cuota_actual = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()
        
    else:
        cuota_actual = PaymentPlan.objects.filter(
            credit_id__id=credito.id,
            start_date__lte=dia,
            fecha_limite__gte=dia_mas_uno
        ).first()

    
    if cuota_actual is None:
        cuota_actual = PaymentPlan.objects.filter(
        credit_id__id=credito.id).order_by('-id').first()

    return cuota_actual 

def cuota_siguiente(credito):
    # 1. Obtenemos la cuota actual usando tu lógica existente
    cuota_actual = cuota(credito)
    
    if not cuota_actual:
        return None

    # 2. Buscamos la cuota que sigue en el plan de pagos
    # Asumiendo que el orden lógico es por fecha de inicio o por ID
    proxima = PaymentPlan.objects.filter(
        credit_id__id=credito.id,
        start_date__gt=cuota_actual.start_date # Que empiece después de la actual
    ).order_by('start_date').first()
    
    return proxima