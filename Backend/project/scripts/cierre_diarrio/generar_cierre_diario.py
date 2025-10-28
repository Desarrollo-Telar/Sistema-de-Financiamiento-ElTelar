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
from .informacion_relacionado_cliente import generando_informacion_cliente

def generando_informe_cierre_diario(dia =  datetime.now().date()):
    log_system_event(
        'Generando el cierre diario',
        'INFO',
        'Sistema',
        'General'
    )

    informe = InformeDiarioSistema.objects.get_or_create(
        fecha_registro=dia
    )

    for sucursal in Subsidiary.objects.all().order_by('id'):
        DetalleInformeDiario.objects.create(
            reporte=informe,
            data=generando_informacion_cliente(sucursal)
        ) 
    