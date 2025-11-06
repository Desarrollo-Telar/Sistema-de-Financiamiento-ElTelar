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







def generando_informe_cierre_diario(dia=None):
    if dia is None:
        dia = datetime.now().date()



def generar_cierre_diario(dia=None):
    if dia is None:
        dia = datetime.now().date()

    inicio = time.perf_counter()

    log_system_event('Generando el cierre diario', 'INFO', 'Sistema', 'General')

    informes_generados = 0

    for sucursal in Subsidiary.objects.all().order_by('id').iterator(chunk_size=500):
        with transaction.atomic():
            informe, creado = InformeDiarioSistema.objects.get_or_create(
                fecha_registro=dia,
                sucursal=sucursal
            )

            

            data_map = {
                'clientes': generando_informacion_cliente(sucursal),
            }

            # 🔹 Guardar cada tipo de datos
            for key, value in data_map.items():
                DetalleInformeDiario.objects.create(
                    reporte=informe,
                    data={key: value},   # JSONField
                    tipo_datos=key,
                    cantidad=len(value)
                )

            informes_generados += 1
            del serializer, clientes_serializados, clientes_json, clientes_data, data_map
            gc.collect()

    log_system_event(
        f'Cierre diario generado correctamente ({informes_generados} sucursales procesadas)',
        'SUCCESS',
        'Sistema',
        'General'
    )

    fin = time.perf_counter()
    print(f"⏳ Tiempo total de ejecución: {fin - inicio:.2f} segundos")

    return f'Cierre diario completado para {informes_generados} sucursales ({dia})'


def generar_cierre_diario_seguro():
    print(gc.get_stats())  # antes
    gc.collect()  # 🔹 Limpia objetos no referenciados de memoria
    
    generar_cierre_diario()  # tu función principal
    print(gc.get_stats())  # antes
    gc.collect()  # 🔹 Vuelve a limpiar al final

