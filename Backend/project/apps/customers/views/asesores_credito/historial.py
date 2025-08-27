from django.shortcuts import render, get_object_or_404, redirect

# Modelos
from apps.customers.models import HistorialCobranza, Cobranza
from apps.actividades.models import Informe, DetalleInformeCobranza
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# MENSAJES
from django.contrib import messages

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.recoleccion_informacion.detalle_asesor_credito import recoleccion_informacion_detalle_asesor

# LIBRERIAS PARA CRUD
from django.views.generic import TemplateView, ListView, DetailView

# Tiempo
from datetime import datetime


@login_required
def view_historial_cobranza(request,id):
    template_name = 'cobranza/historial.html'
    get_cobrazana = Cobranza.objects.filter(id=id).first()
    get_detalle = DetalleInformeCobranza.objects.filter(cobranza=get_cobrazana).first()

    if get_cobrazana is None:
        return redirect('index')

    list_historial = HistorialCobranza.objects.filter(cobranza=get_cobrazana)
    context = {
        'permisos': recorrer_los_permisos_usuario(request),
        'list_historial':list_historial,
        'get_cobrazana':get_cobrazana,
        'get_detalle':get_detalle
    }

    return render(request, template_name, context)
