# ADMIN
from django.contrib import admin

# Modelos
from apps.actividades.models import Informe, DetalleInformeCobranza


INFORMEADMIN = admin.site.register(Informe)