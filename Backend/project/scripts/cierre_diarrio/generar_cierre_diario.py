# Modelo
from apps.actividades.models import InformeDiarioSistema, DetalleInformeDiario, ModelHistory
from apps.subsidiaries.models import Subsidiary
from apps.documents.models import DocumentSistema
from apps.users.models import User

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# CONSULTAS
from django.db.models import Q
from django.db import transaction

# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now
import time, gc, os, json

# Recolecion de informacion
from .informacion_relacionado_cliente import generando_informacion_cliente
from .informacion_relacionada_credito import obtener_informacion_creditos
from .informacion_relacionada_bancos import generar_informacion_bancos, generar_informacion_recibos, generar_informacion_facturas, generar_informacion_pagos


def generar_cierre_diario(dia=None):
    if dia is None:
        dia = datetime.now().date()

    inicio = time.perf_counter()

    log_system_event('Generando el cierre diario', 'INFO', 'Sistema', 'General')

    sucursales = Subsidiary.objects.all()
    informes_generados = sucursales.count()

    for sucursal in sucursales:
      ejecutar_cierre_diario(dia, sucursal.id)


    log_system_event(
        f'Cierre diario generado correctamente ({informes_generados} sucursales procesadas)',
        'SUCCESS',
        'Sistema',
        'General'
    )

    fin = time.perf_counter()
    tiempo = fin - inicio
    minutos = tiempo // 60
    segundos = tiempo % 60

    print(f"Tiempo total: {tiempo:.4f} segundos ({int(minutos)} min {segundos:.2f} seg)")
    
    return f'Cierre diario completado para {informes_generados} sucursales ({dia})'


def generar_cierre_diario_seguro():
    print(gc.get_stats())  
    gc.collect()  
    
    generar_cierre_diario()  

    print(gc.get_stats())  
    gc.collect()  

from django.db import connection, transaction

def ejecutar_cierre_diario(dia=None, sucursal_id=1):

    if dia is None:
        dia = datetime.now().date()

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(
                "CALL generar_informe_diario(%s, %s)",
                [dia, sucursal_id]
            )
