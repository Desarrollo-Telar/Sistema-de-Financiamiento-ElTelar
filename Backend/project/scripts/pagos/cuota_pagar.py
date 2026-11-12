
# FUNCIONES
from .sobre_que_pago_analizar import sobre_que_es_pago


# Tiempo
from datetime import datetime,timedelta



from django.db.models import Q


def obtener_cuota_vigente(self,objeto, fecha_emision=None):
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
            return self.get_plan_pagos().objects.filter(**filtro_relacion).order_by('-id').first()

    elif hasattr(objeto, 'acreedor'):   # Es un objeto Creditor o similar
        filtro_relacion = {'acreedor': objeto}
    elif hasattr(objeto, 'seguro'):     # Es un objeto Insurance o similar
        filtro_relacion = {'seguro': objeto}
    else:
        # Si se pasa la relación directa en un kwargs/diccionario
        filtro_relacion = objeto

    # Buscar la cuota dentro del rango de la fecha especificada
    # Usamos lt para replicar la lógica de excluir la fecha_limite exacta si es necesario
    cuota_actual = self.get_plan_pagos().objects.filter(
        start_date__date__lte=fecha_emision,
        fecha_limite__date__gt=fecha_emision,
        **filtro_relacion
    ).first()

    # Fallback: Si no se encuentra una cuota activa en el rango, obtiene la más reciente
    if not cuota_actual:
        cuota_actual = self.get_plan_pagos().objects.filter(**filtro_relacion).order_by('-id').first()

    return cuota_actual

def cuota_a_pagar(self):
    # Obtener todas las cuotas del crédito ordenadas por la fecha límite
    informacion = sobre_que_es_pago(self)

    # Fecha de emisión (como objeto datetime)
    fecha_emision = self.fecha_emision.date()

    if self._tiene_descuento() is not None:
        return self._tiene_descuento().cuota
    

    if informacion['ultimo_registro_estado_cuenta'] is not None:
        ultima_fecha = informacion['ultimo_registro_estado_cuenta'].payment.fecha_emision.date()
            

        # Calcular la diferencia en días
        diferencia = (ultima_fecha - fecha_emision).days
        print(f"Diferencia en días desde el último pago: {diferencia} días")

        # Si han pasado 15 días desde el último pago
        if diferencia >= 15:
            # Devolver la cuota más reciente impaga
            print('COBRANDO LA ULTIMA CUOTA POR DIFERENCIA DE DÍAS >= 15')
                
            return informacion['ultima_cuota_pagar']
    
   

    cuota_no_encontrada = obtener_cuota_vigente(self, informacion['credito'] , fecha_emision)

    if cuota_no_encontrada:
        print(f"Cuota encontrada fuera del rango de fechas: {cuota_no_encontrada}")
        return cuota_no_encontrada

        
    # Si no se encuentra ninguna cuota aplicable
    print("No se encontró ninguna cuota aplicable")
    return None

    
