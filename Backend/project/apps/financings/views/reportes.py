
# ...abs
from django.shortcuts import render, redirect

# Tiempo
from datetime import datetime

# Modelos
from apps.financings.models import Recibo



# Manejador de filtros
from django.db.models import Q, Sum

# REPORTE EXCEL
from project.reports_excel import report_pagos
from apps.financings.formato import formatear_numero

# SCRIPT
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

def reportes_generales(request):
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
    #filters &= Q(pago__registro_ficticio=False)
    filters &= Q(pago__credit__isnull=False)

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
            return redirect('report_pagos_generales',str(anio), str(mes))
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
        return redirect('financings:reportes')

    # Calcular el total del campo seleccionado
    total_seleccionado = 0
    if filtro_seleccionado in filtros_validos:
        total_seleccionado = reportes.aggregate(Sum(filtro_seleccionado))[f'{filtro_seleccionado}__sum'] or 0
    
    to = formatear_numero(total_seleccionado)

    context = {
        'title': f'Reporte de los pagos a los creditos. {filtro_seleccionado}',
        'posicion': f'CREDITOS / {filtro_seleccionado}',
        'reportes': reportes,
        'filters':filters,
        'mes': mes,
        'anio': anio,
        'filtro_seleccionado': filtro_seleccionado,
        'total_seleccionado': to,
        'total':formatear_numero(total),
        'descarga_credito':True,
        'permisos':recorrer_los_permisos_usuario(request)
    }
    return render(request, template_name, context)

