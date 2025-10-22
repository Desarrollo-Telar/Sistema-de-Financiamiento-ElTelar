
# ...abs
from django.shortcuts import render,  redirect

# Tiempo
from datetime import datetime

# Modelos
from apps.financings.models import Recibo


# Manejador de filtros
from django.db.models import Q, Sum
from apps.financings.formato import formatear_numero

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Decoradores
from project.decorador import permiso_requerido

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

@permiso_requerido('puede_descargar_reporte_acreedores')
def reportes_generales_acreedores(request):
    template_name = 'reports/base.html'
    mes = datetime.now().month
    anio = datetime.now().year
    filtro_seleccionado = 'mora_pagada'  # Valor predeterminado
    total = 0

    if request.method == 'POST':
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        filtro_seleccionado = request.POST.get('filtro')

        # Validación de mes y año
        if not mes:
            mes = datetime.now().month
        else:
            mes = int(mes)

        if not anio:
            anio = datetime.now().year
        else:
            anio = int(anio)

    # Filtros por fecha
    filters = Q()
    filters &= Q(fecha__year=anio)
    filters &= Q(fecha__month=mes)
    filters &= Q(pago__registro_ficticio=False)
    filters &= Q(pago__acreedor__isnull=False)

    # Filtro dinámico según selección del usuario
    filtros_validos = {
        'mora_pagada': 'mora_pagada__gt',
        'interes_pagado': 'interes_pagado__gt',
        'aporte_capital': 'aporte_capital__gt',
        'general':'general',
    }
    reportes = None
    if filtro_seleccionado in filtros_validos:
        if filtro_seleccionado == 'general':
            return redirect('report_pagos_generales_acreedores',str(anio), str(mes))
        
        filtro_dinamico = {filtros_validos[filtro_seleccionado]: 0}
        
        
        reportes = Recibo.objects.filter(filters).filter(**filtro_dinamico)
        for reporte in reportes:
            if filtro_seleccionado == 'mora_pagada':
                total += reporte.mora_pagada
            elif filtro_seleccionado == 'interes_pagado':
                total += reporte.interes_pagado
            else:
                total += reporte.aporte_capital
            
 
    else:
        return redirect('contable:reportes_acreedores')

    # Calcular el total del campo seleccionado
    total_seleccionado = 0
    if filtro_seleccionado in filtros_validos:
        total_seleccionado = reportes.aggregate(Sum(filtro_seleccionado))[f'{filtro_seleccionado}__sum'] or 0
    
    to = formatear_numero(total_seleccionado)

    context = {
        'title': 'Reporte de pagos sobre los acreedores.',
        'posicion': f'ACREEDORES / {filtro_seleccionado}',
        'reportes': reportes,
        'filters':filters,
        'mes': mes,
        'anio': anio,
        'filtro_seleccionado': filtro_seleccionado,
        'total_seleccionado': to,
        'total':formatear_numero(total),
        'descarga_acreedor':True,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

@permiso_requerido('puede_descargar_reporte_seguros')
def reportes_generales_seguros(request):
    template_name = 'reports/base.html'
    mes = datetime.now().month
    anio = datetime.now().year
    filtro_seleccionado = 'mora_pagada'  # Valor predeterminado
    total = 0

    if request.method == 'POST':
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        filtro_seleccionado = request.POST.get('filtro')

        # Validación de mes y año
        if not mes:
            mes = datetime.now().month
        else:
            mes = int(mes)

        if not anio:
            anio = datetime.now().year
        else:
            anio = int(anio)

    # Filtros por fecha
    filters = Q()
    filters &= Q(fecha__year=anio)
    filters &= Q(fecha__month=mes)
    filters &= Q(pago__registro_ficticio=False)
    filters &= Q(pago__seguro__isnull=False)

    # Filtro dinámico según selección del usuario
    filtros_validos = {
        'mora_pagada': 'mora_pagada__gt',
        'interes_pagado': 'interes_pagado__gt',
        'aporte_capital': 'aporte_capital__gt',
        'general':'general',
    }
    reportes = None
    if filtro_seleccionado in filtros_validos:
        if filtro_seleccionado == 'general':
            return redirect('report_pagos_generales_seguros',str(anio), str(mes))
        filtro_dinamico = {filtros_validos[filtro_seleccionado]: 0}
        
        reportes = Recibo.objects.filter(filters).filter(**filtro_dinamico)
        for reporte in reportes:
            if filtro_seleccionado == 'mora_pagada':
                total += reporte.mora_pagada
            elif filtro_seleccionado == 'interes_pagado':
                total += reporte.interes_pagado
            else:
                total += reporte.aporte_capital
            
 
    else:
        return redirect('contable:reportes_seguros')

    # Calcular el total del campo seleccionado
    total_seleccionado = 0
    if filtro_seleccionado in filtros_validos:
        total_seleccionado = reportes.aggregate(Sum(filtro_seleccionado))[f'{filtro_seleccionado}__sum'] or 0
    
    to = formatear_numero(total_seleccionado)

    context = {
        'title': 'Reporte de pagos de seguros.',
        'posicion': f'SEGUROS / {filtro_seleccionado}',
        'reportes': reportes,
        'filters':filters,
        'mes': mes,
        'anio': anio,
        'filtro_seleccionado': filtro_seleccionado,
        'total_seleccionado': to,
        'total':formatear_numero(total),
        'descarga_seguro':True,
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
    return render(request, template_name, context)
