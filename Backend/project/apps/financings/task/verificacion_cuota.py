# CELERY
from celery import shared_task

# SCRIPTS
from scripts.manejo_contador_por_dias import ejecutar_max_1_veces_al_dia
from scripts.cuotas.cuotas_fecha_vencimiento import verificador_de_cuotas_vencidas
from scripts.cuotas.cuotas_fecha_limite import verificador_de_cuotas_fecha_limite
from scripts.cuotas.cuotas_por_vencerse import cuotas_por_vencerse_alerta

# TIEMPO
from datetime import datetime, time
from django.utils.timezone import now


# SETTINGS
from project.settings import SERVIDOR

@shared_task(name="apps.financings.task.cambiar_plan")
def cambiar_plan():
    validacion = ejecutar_max_1_veces_al_dia()
    dia = datetime.now().date()
    
    if not SERVIDOR:
        return
    
    if not validacion:
        return
    
    
    print(f'VERIFICACION DE CUOTAS POR FECHA DE VENCIMIENTO')
    verificador_de_cuotas_vencidas(dia)
    print()
    print(f'VERIFICACION DE CUOTAS POR FECHA LIMITE')
    verificador_de_cuotas_fecha_limite(dia)
    print()
    print(f'VERIFICACION DE PROXIMAS CUOTAS')
    
    cuotas_por_vencerse_alerta()

