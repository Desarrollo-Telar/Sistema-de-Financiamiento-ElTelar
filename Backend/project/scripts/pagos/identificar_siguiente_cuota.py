
# DJANGO
from django.db.models import Q

# FUNCIONES
from .sobre_que_pago_analizar import sobre_que_es_pago
from .cuota_pagar import obtener_cuota_vigente


def obtener_siguiente_cuota(self,objeto, cuota_actual=None, fecha_emision=None):
    # Obtener la cuota vigente si no se proporciona
    if cuota_actual is None:
        cuota_actual = obtener_cuota_vigente(self,objeto, fecha_emision)

    if cuota_actual is None:
        return None

    # Identificar el tipo de relación
    if isinstance(objeto, dict):
        filtro_relacion = objeto

    elif hasattr(objeto, 'is_paid_off'):
        filtro_relacion = {'credit_id': objeto}

    elif hasattr(objeto, 'acreedor'):
        filtro_relacion = {'acreedor': objeto}

    elif hasattr(objeto, 'seguro'):
        filtro_relacion = {'seguro': objeto}

    else:
        raise ValueError("Tipo de objeto no válido")

    # Buscar la siguiente cuota disponible
    siguiente_cuota = self.get_plan_pagos().objects.filter(
        **filtro_relacion,
        id__gt=cuota_actual.id
    ).order_by('id').first()

    return siguiente_cuota


def encontrando_siguiente_cuota(self):
    cuota_actual = self._cuota_pagar()

    if cuota_actual is not None:
        fecha_emision = self.fecha_emision.date()
        informacion = sobre_que_es_pago(self)

        siguiente_cuota = obtener_siguiente_cuota(self, objeto=informacion['credito'], cuota_actual=cuota_actual, fecha_emision=fecha_emision)

        if siguiente_cuota is not None:
            return siguiente_cuota

    return None  # Si no existe una siguiente cuota
