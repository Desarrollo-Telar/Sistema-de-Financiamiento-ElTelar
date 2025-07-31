
# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now

# Modelos
from apps.actividades.models import Informe

def ver_estado_informe(dia):
    ver_informes = Informe.objects.filter(fecha_vencimiento = dia)

    if not ver_informes.exists():
        return

    for informe in ver_informes:
        informe.esta_activo = False
        informe.save()