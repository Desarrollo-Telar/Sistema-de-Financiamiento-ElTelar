from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Customer, CreditCounselor
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

@login_required
@permiso_requerido('puede_visualizar_detalle_asesor_credito')
def detail_asesor(request, codigo_asesor):
    template_name = 'asesores_credito/detail.html'
    asesor_credito = CreditCounselor.objects.filter(codigo_asesor=codigo_asesor).first()

    if asesor_credito is None:
        return redirect('http_404')
    
    context = {
        'title': f'{codigo_asesor}',
        'asesor_credito': asesor_credito,
        'informacion_asesor':recoleccion_informacion_detalle_asesor(asesor_credito),
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

@login_required
def detail_informe(request, user_code, id):
    template_name = 'cobranza/detail.html'
    reporte = Informe.objects.filter(id=id ).first()

    if reporte is None:
        return redirect('http_404')
    
    detalles_informe = DetalleInformeCobranza.objects.filter(reporte=reporte)

    context = {
        'title': f'COBRANZA | INFORME | {user_code} | {reporte.fecha_registro} - {reporte.fecha_vencimiento} |',
        'report':reporte,
        'object_list':detalles_informe,
        'permisos':recorrer_los_permisos_usuario(request),
        'posicion': f'{reporte.nombre_reporte}'
    }

    return render(request, template_name, context)