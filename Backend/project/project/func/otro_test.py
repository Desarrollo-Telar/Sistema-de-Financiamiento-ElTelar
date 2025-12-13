import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now

from scripts.cierre_diarrio.informacion_relacionado_cliente import generando_informacion_cliente
from scripts.manejo_excedentes.recalcular import cuotas_con_excedente
from scripts.cierre_diarrio.generar_cierre_diario import  generar_cierre_diario_seguro


from apps.customers.models import CreditCounselor, Cobranza, Customer
from apps.financings.models import Credit
from apps.actividades.models import Informe, DetalleInformeCobranza, ModelHistory
from datetime import date
from scripts.conversion_datos import model_to_dict, cambios_realizados
from django.apps import apps
from apps.subsidiaries.models import Subsidiary
import uuid
from django.db.models import Q

def pruebas(dia, sucursal):
   from django.db import connection

   with connection.cursor() as cursor:
      cursor.execute("CALL generar_informe_diario(%s, %s)", [dia, sucursal.id])


if __name__ == '__main__':
   # Obtener el mes
   dia = datetime.now().date()
   mes = dia.month
   nombre_mes = dia.strftime("%B")

   print(f"El nombre del mes actual es: {nombre_mes}")

   # Obtener todas las cobranzas con estado diferente de pendiente
   filtros = Q()
   filtros &= Q(estado_cobranza__icontains = 'INCUMPLIDO')
   filtros &= Q(fecha_registro__month = mes)
   
   cobranzas = Cobranza.objects.filter(filtros)

   for cobranza in cobranzas:
      fecha_seguimiento = cobranza.fecha_seguimiento.date() if cobranza.fecha_seguimiento else None
      fecha_promesa_pago = cobranza.fecha_promesa_pago

      if fecha_promesa_pago:
         if dia < fecha_promesa_pago:
            print(f'Cobranza: {cobranza}: Asesor:{cobranza.asesor_credito}\nFecha Seguimiento: {fecha_seguimiento}, Fecha Promesa de Pago: {fecha_promesa_pago}. Comprobar: {fecha_promesa_pago < dia if fecha_promesa_pago else None}')
            cobranza.estado_cobranza = 'PENDIENTE'
            cobranza.resultado = 'Promesa de pago'
            #cobranza.save()
   
  