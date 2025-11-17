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


from apps.customers.models import CreditCounselor, Cobranza
from apps.actividades.models import Informe, DetalleInformeCobranza, ModelHistory
from datetime import date
from scripts.conversion_datos import model_to_dict, cambios_realizados
from django.apps import apps
if __name__ == '__main__':
   content_type = 'actividades.DetalleInformeCobranza'

   asesor = CreditCounselor.objects.get(id= 4)

   informe_activo = Informe.objects.filter(usuario=asesor.usuario, fecha_vencimiento='2025-11-01' ,esta_activo = False).order_by('-id').first()
   
   anio = 2025
   mes = 11
   

   cobranzas_realizadas = Cobranza.objects.filter(asesor_credito=asesor,fecha_registro__year=anio,fecha_registro__month=mes)
   

   if cobranzas_realizadas is not None:
      for cobranza_hecha in cobranzas_realizadas:

         detalles = DetalleInformeCobranza.objects.filter(
            reporte=informe_activo,
            cobranza=cobranza_hecha
         )

         if detalles is None:
            continue

         for detalle in detalles:
            ModelHistory.objects.create(
                  content_type=content_type,
                  object_id=detalle.id,
                  action='delete',
                  data=model_to_dict(detalle),
                  notes='Por fallas de sistema, no se hizo el cambio para el reporte del informe mensual, por el cual se estan traslando al informe del mes de noviembre todas las operaciones que fueron mezcladas con el mes de octubre'
            )
            detalle.delete()

   
         
   

            


   

   


        

    
    
    

    