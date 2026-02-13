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

      saldo_capital += cuota_actual.saldo_pendiente


   informacion_actual['saldo_capital'] = saldo_capital
    
   

   return informacion_actual 


if __name__ == '__main__':
   # consulta_receptor('11024163-0')
   # {'nit': '11024163-0', 'nombre': '', 'mensaje': 'NIT no válido'}
   sucursal = Subsidiary.objects.get(id=1)

   base_credit_filter = {"sucursal": sucursal, "is_paid_off": False}
   creditos = Credit.objects.filter(estados_fechas=False, **base_credit_filter).exclude(estado_judicial=True)
   print(cuota(creditos).get('saldo_capital'))
