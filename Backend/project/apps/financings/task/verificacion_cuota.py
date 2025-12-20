# CELERY
from celery import shared_task

# SCRIPTS
from scripts.manejo_contador_por_dias import ejecutar_max_1_veces_al_dia
from scripts.cuotas.cuotas_fecha_vencimiento import verificador_de_cuotas_vencidas
from scripts.cuotas.cuotas_fecha_limite import verificador_de_cuotas_fecha_limite
from scripts.cuotas.cuotas_por_vencerse import cuotas_por_vencerse_alerta
from scripts.recordatorios.informes import ver_estado_informe
from scripts.recordatorios.cobranzas import fechas_cobranzas
from scripts.cierre_diarrio.generar_cierre_diario import  generar_cierre_diario_seguro
# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now

# Modelos
from apps.actividades.models import Informe

# SETTINGS
from project.settings import SERVIDOR



def ver_cuotas(dia):
    print(f'VERIFICACION DE CUOTAS POR FECHA DE VENCIMIENTO')
    verificador_de_cuotas_vencidas(dia)
    print()
    print(f'VERIFICACION DE CUOTAS POR FECHA LIMITE')
    verificador_de_cuotas_fecha_limite(dia)
    print()
    print(f'VERIFICACION DE PROXIMAS CUOTAS')
    cuotas_por_vencerse_alerta()
    print()
    
    print()



@shared_task(name="apps.financings.task.cambiar_plan")
def cambiar_plan():
    validacion = ejecutar_max_1_veces_al_dia()
    dia = datetime.now().date()
    
    if not SERVIDOR:
        return
    
    if not validacion:
        return
    
    ver_cuotas(dia)
    ver_estado_informe(dia)
    fechas_cobranzas()
    generar_cierre_diario_seguro()

    

