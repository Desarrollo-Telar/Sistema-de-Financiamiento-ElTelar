from django.shortcuts import render, get_object_or_404, redirect



# Models
from apps.customers.models import Customer, CreditCounselor
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# MENSAJES
from django.contrib import messages

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

@login_required
@permiso_requerido('puede_visualizar_detalle_asesor_credito')
def detail_asesor(request, codigo_asesor):
    pass