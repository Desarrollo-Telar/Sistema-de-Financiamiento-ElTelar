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

# modelos
from apps.financings.models import PaymentPlan



if __name__ == '__main__':

    for cuota in PaymentPlan.objects.filter(credit_id__isnull=False):
        original_day = cuota.credit_id.fecha_inicio.day
        cuota.original_day = original_day
        cuota.save()
        print(original_day)
    


        

    
    
    

    