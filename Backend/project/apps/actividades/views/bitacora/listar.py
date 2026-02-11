from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.actividades.models import ModelHistory

# Decoradores
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator



# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Manejo de mensajes
from django.contrib import messages

# Tiempo
from datetime import datetime, timedelta

# financings.Credit

def historial(request):
    template_name = 'bitacora/index.html'
    filters = Q()
    term_content_type = request.GET.get('content_type')
    term_object_id = request.GET.get('object_id')

    if term_content_type:
        filters &= Q(content_type = term_content_type)
    
    if term_object_id:
        filters &= Q(object_id = term_object_id)


    histories = ModelHistory.objects.filter(filters).order_by('-timestamp')

    context = {
        'histories' : histories,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)