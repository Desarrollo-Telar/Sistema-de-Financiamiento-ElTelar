from apps.financings.models import Banco, Payment, Recibo
from openpyxl import Workbook
from django.http import HttpResponse



import json
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q, Sum

def report_pagos(request, filtro_seleccionado, anio, mes, total):
    # Mapeo de filtros válidos
    filtros_validos = {
        'mora_pagada': 'mora_pagada__gt',
        'interes_pagado': 'interes_pagado__gt',
        'aporte_capital': 'aporte_capital__gt',
    }
    filters = Q()
    filters &= Q(fecha__year=anio)
    filters &= Q(fecha__month=mes)
    #filters &= Q(pago__registro_ficticio=False)
    filters &= Q(pago__credit__isnull=False)

   

    # Filtrar los reportes
    reportes = None
    
    # Si el filtro seleccionado es válido, aplicar el filtro adicional
    if filtro_seleccionado in filtros_validos:
        filtro_dinamico = {filtros_validos[filtro_seleccionado]: 0}
        reportes = Recibo.objects.filter(filters).filter(**filtro_dinamico)
        

    # Crear el archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"Reporte de {filtro_seleccionado}"

    # Agregar encabezados
    sheet['A1'] = f'REPORTE SOBRE {filtro_seleccionado}'
    sheet['F1'] = str(total)
    sheet.append(["#", "FECHA", "CODIGO DEL CREDITO", "CLIENTE", "NO. REFERENCIA", "MONTO PAGADO", "STATUS DEL CREDITO"])

    # Agregar los datos al archivo Excel
    for idx, reporte in enumerate(reportes, start=1):
        monto = None

        # Seleccionar el monto correcto según el filtro
        if filtro_seleccionado == 'mora_pagada':
            monto = reporte.mora_pagada
        elif filtro_seleccionado == 'interes_pagado':
            monto = reporte.interes_pagado
        elif filtro_seleccionado == 'aporte_capital':
            monto = reporte.aporte_capital

        # Agregar los datos a la fila correspondiente
        mensaje = None
        if reporte.pago.credit.estado_aportacion:
            mensaje = 'VIGENTE'
        elif reporte.pago.credit.estado_aportacion is None:
            mensaje = 'SIN APORTACIONES'
        else:
            mensaje = 'EN ATRASO'

        aportacion = mensaje
        s_fecha = 'VIGENTE' if reporte.pago.credit.estados_fechas else 'EN ATRASO'
        sheet.append([
            idx, 
            str(reporte.fecha),
            str(reporte.pago.credit.codigo_credito),
            str(reporte.cliente),
            str(reporte.pago.numero_referencia),
            str(monto),
            f"Status de Aportación: {aportacion}, "
            f"Status por Fecha: {s_fecha}"
        ])

    # Crear respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="reportes_sobre_pagos_{filtro_seleccionado}.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response
