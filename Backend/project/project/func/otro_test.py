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
from scripts.cierre_diarrio.generar_cierre_diario import  generar_cierre_diario_seguro, ejecutar_cierre_diario, generar_cierre_diario
from scripts.INFILE.consulta_nit import consulta_receptor

from apps.customers.models import CreditCounselor, Cobranza, Customer
from apps.financings.models import Credit, PaymentPlan, Recibo
from apps.actividades.models import Informe, DetalleInformeCobranza, ModelHistory, DetalleInformeDiario


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
        credito.saldo_pendiente = cuota_actual.saldo_pendiente
        credito.save()


   informacion_actual['saldo_capital'] = saldo_capital
    
   

   return saldo_capital

from django.db.models import Sum, OuterRef, Subquery, Q, DecimalField, Case, When
from django.db.models.functions import Coalesce
from django.db.models import Sum, OuterRef, Subquery, Q, DecimalField
from django.db.models.functions import Coalesce

from django.db.models import Sum, Q, DecimalField, Case, When
from django.db.models.functions import Coalesce

def obtener_cartera_por_asesor(sucursal_id):
    # 1. Definimos los filtros de créditos "limpios" (sin procesos judiciales)
    filtros_limpios = Q(
        sucursal_id=sucursal_id,
        is_paid_off=False,
        estado_judicial=False,
        categoria_credito_demandado__isnull=True
    )

    # 2. Consulta agrupada por asesor usando el campo saldo_pendiente de Credit
    data = (
        Credit.objects.filter(filtros_limpios)
        .values('asesor_de_credito__nombre', 'asesor_de_credito__apellido')
        .annotate(
            # Sumamos directamente el campo del modelo Credit
            saldo_cartera_total=Coalesce(
                Sum('saldo_pendiente'), 
                0, 
                output_field=DecimalField()
            ),
            # Sumamos el saldo_pendiente solo si el crédito está en atraso
            saldo_en_atraso=Coalesce(
                Sum(
                    Case(
                        When(estados_fechas=False, then='saldo_pendiente'),
                        default=0,
                        output_field=DecimalField()
                    )
                ),
                0, 
                output_field=DecimalField()
            )
        )
        .order_by('-saldo_cartera_total')
    )
    
    return data

if __name__ == '__main__':
   datos = obtener_cartera_por_asesor(1)

   saldo_total_v = 0
   saldo_total_a = 0

   for fila in datos:
      print(f"Asesor: {fila['asesor_de_credito__nombre'] } {fila['asesor_de_credito__apellido']}")
      print(f"Cartera Total: Q{fila['saldo_cartera_total']}")
      print(f"En Atraso: Q{fila['saldo_en_atraso']}")
      saldo_total_v += fila['saldo_cartera_total']
      saldo_total_a += fila['saldo_en_atraso']
      print("-" * 20)
   
   
  

  
