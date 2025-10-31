# URLS
from django.shortcuts import render, redirect

# TIEMPO
from datetime import datetime, timedelta

# Models
from apps.actividades.models import UserLog, SystemLog, LogCategory, LogLevel

# Manejo de mensajes
from django.contrib import messages

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q
from itertools import chain
from operator import attrgetter
# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido, usuario_activo
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario



from django.core.paginator import Paginator

@login_required
@usuario_activo
def listar_cierre_diario(request):
    template_name = 'cierre_diario/reportes_cierre.html'
    context = {
        'permisos': recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)