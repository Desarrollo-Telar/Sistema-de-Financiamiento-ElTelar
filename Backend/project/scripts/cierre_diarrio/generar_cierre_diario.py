# Modelo
from apps.actividades.models import InformeDiarioSistema, DetalleInformeDiario, ModelHistory
from apps.subsidiaries.models import Subsidiary

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados


# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now

# FUNCIONES
from .informacion_relacionado_cliente import generando_informacion_cliente, obtener_informacion_creditos_sucursal
from .informacion_relacionada_bancos import generar_informacion_bancos, generar_informacion_recibos, generar_informacion_pagos, generar_informacion_facturas
from .informacion_relacionado_contable import generar_informacion_acreedores, generar_informacion_seguros, generar_informacion_ingresos, generar_informacion_egresos

from datetime import datetime
from django.db import transaction


def generando_informe_cierre_diario(dia=None):
    if dia is None:
        dia = datetime.now().date()

    log_system_event(
        'Generando el cierre diario',
        'INFO',
        'Sistema',
        'General'
    )

    informes_generados = 0

    with transaction.atomic():
        for sucursal in Subsidiary.objects.all().order_by('id'):
            informe, creado = InformeDiarioSistema.objects.get_or_create(
                fecha_registro=dia,
                sucursal=sucursal
            )

            data_map = {
                #'clientes': generando_informacion_cliente(sucursal, dia),
                'creditos':obtener_informacion_creditos_sucursal(sucursal, dia),
                #'bancos': generar_informacion_bancos(sucursal),
                #'recibos': generar_informacion_recibos(sucursal),
                #'pagos': generar_informacion_pagos(sucursal),
                #'facturas': generar_informacion_facturas(sucursal),
                #'acreedores': generar_informacion_acreedores(sucursal),
                #'seguros': generar_informacion_seguros(sucursal),
                #'ingresos': generar_informacion_ingresos(sucursal),
                #'egresos': generar_informacion_egresos(sucursal),
            }

            # Crear los detalles del informe
            for key, value in data_map.items():
                DetalleInformeDiario.objects.create(
                    reporte=informe,
                    data={key: value},
                    tipo_datos = key,
                    cantidad = len(value)
                )

            informes_generados += 1

    log_system_event(
        f'Cierre diario generado correctamente ({informes_generados} sucursales procesadas)',
        'SUCCESS',
        'Sistema',
        'General'
    )

    return f'Cierre diario completado para {informes_generados} sucursales ({dia})'


