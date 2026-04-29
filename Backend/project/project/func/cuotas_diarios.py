import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


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
from apps.financings.models import Recibo
from apps.customers.models import Cobranza
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

from django.db import connection

def actualizar_cobranza_masiva():
    query = """
    UPDATE customers_cobranza AS cobranza
    SET estado_cobranza = %s, 
        resultado = %s
    FROM financings_credit AS credito
    WHERE credito.id = cobranza.credito_id
      AND cobranza.estado_cobranza IN ('PENDIENTE', 'INCUMPLIDO')
      AND cobranza.cuota_id IN (SELECT cuota_id FROM financings_recibo)
      AND credito.estados_fechas = TRUE;
    """
    
    with connection.cursor() as cursor:
        # Pasamos los valores como parámetros para evitar SQL Injection
        cursor.execute(query, ['COMPLETADO', 'Pago realizado'])
        
        # Opcional: obtener cuántas filas se afectaron
        row_count = cursor.rowcount
        
    return row_count

def cobran():
    actualizar_cobranza_masiva()

from decimal import Decimal

def calculo_interes_acumulado(tasa_interes, saldo_capital_pendiente, n):
    # Convertimos a Decimal para precisión financiera
    tasa = Decimal(str(tasa_interes))
    saldo = Decimal(str(saldo_capital_pendiente))
    interes_acumulado = Decimal('0')
    
    i = 0
    # Cambiamos == por < para que el ciclo funcione
    while i < n:
        # El interés del mes actual sobre el saldo pendiente
        interes_del_mes = saldo * tasa
        interes_acumulado += interes_del_mes
        
        # El saldo aumenta porque el interés se capitaliza
        saldo += interes_del_mes
        
        i += 1
        print(f'MES: {i}, Interés del mes: {interes_del_mes:.2f}, Acumulado: {interes_acumulado:.2f}')
    
    return interes_acumulado




def cambiar_plan():
    #validacion = ejecutar_max_1_veces_al_dia()
    dia = '2026-03-25'
    
    
    from datetime import datetime

    dia = datetime.strptime(dia, "%Y-%m-%d").date()
    
    
    ver_cuotas(dia)
    ver_estado_informe(dia)
    generar_cierre_diario_seguro()
    fechas_cobranzas()
    cobran()


if __name__ == '__main__':
    #cambiar_plan()
    print(calculo_interes_acumulado(0.1,10000,3))