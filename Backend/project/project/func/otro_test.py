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


from apps.customers.models import CreditCounselor, Cobranza, Customer
from apps.financings.models import Credit
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


if __name__ == '__main__':
   detalles = DetalleInformeDiario.objects.filter(tipo_datos='creditos', reporte = 114).first()
   #informacion_recibo
   for detalle in detalles.data['creditos']:
      print(type(detalle.get('credito',{}).get('estado_judicial','')))
   
   
      
  

   
   
  