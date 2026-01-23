# DECORADORES
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo

# Recoleccion de datos
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.recoleccion_reporte_dashboard import recolectar_informes_status_creditos, recolectar_informacion_cobranza

# OS
import os

# QR
import qrcode

# SETTINGS OF PROJECT
from django.conf import settings

# Modelos
from apps.customers.models import Customer,CreditCounselor, Cobranza
from apps.actividades.models import UserLog


# URLS
from django.shortcuts import render, redirect

# DJANGO HTTP
from django.http import HttpResponse

@login_required
@usuario_activo
def dashboard(request):
    template_name = 'dashboard/index.html'
    context = {
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)