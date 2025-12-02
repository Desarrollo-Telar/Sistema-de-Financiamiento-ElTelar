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




if __name__ == '__main__':
   cliente = Credit.objects.get(id = 310)
   for fiador in cliente.mi_fiador_es():
      print(fiador.especificaciones['Nombre'])
   
   
         
   

            


   

   


        

    
    
    

    