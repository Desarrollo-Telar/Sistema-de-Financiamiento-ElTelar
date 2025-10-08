from apps.financings.models import Banco, Payment, Recibo
from openpyxl import Workbook
from django.http import HttpResponse



import json
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q, Sum

def report_pagos_generales_acreedores(request, anio, mes):
    filtro_seleccionado = f'BOLETAS GENERALES {mes} {anio}'

    filters = Q()
    filters &= Q(fecha__year=anio)
    filters &= Q(fecha__month=mes)
    filters &= Q(pago__acreedor__isnull=False)

    reportes = Recibo.objects.filter(filters)

     # Crear el archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"Reporte de {filtro_seleccionado}"

    # Agregar encabezados
    sheet['A1'] = f'REPORTE SOBRE {filtro_seleccionado}'
    
    sheet.append(["#", "FECHA", "CODIGO DEL ACREEDOR", "NOMBRE", "NO. REFERENCIA", "MONTO PAGADO", "MORA PAGADA"
                  ,"INTERES PAGADO", "CAPITAL APORTADO","SALDO CAPITAL PENDIENTE","SALDO ACTUAL","STATUS DEL ACREEDOR"])

    # Agregar los datos al archivo Excel
    for idx, reporte in enumerate(reportes, start=1):
        monto = reporte.total

        # Agregar los datos a la fila correspondiente
        mensaje = None
        if reporte.pago.acreedor.estado_aportacion:
            mensaje = 'VIGENTE'
        elif reporte.pago.acreedor.estado_aportacion is None:
            mensaje = 'SIN APORTACIONES'
        else:
            mensaje = 'EN ATRASO'

        aportacion = mensaje
        s_fecha = 'VIGENTE' if reporte.pago.acreedor.estados_fechas else 'EN ATRASO'
        sheet.append([
            idx, 
            str(reporte.fecha),
            str(reporte.pago.acreedor.codigo_acreedor),
            str(reporte.pago.acreedor.nombre_acreedor),
            str(reporte.pago.numero_referencia),
            str(reporte.Ftotal()),
            str(reporte.Fmora_pagada()),
            str(reporte.Finteres_pagado()),
            str(reporte.Faporte_capital()),
            str(reporte.cuota.acreedor.formato_saldo_pendiente()),
            str(reporte.cuota.acreedor.formato_saldo_actual()),
            f"Status de Aportación: {aportacion}, "
            f"Status por Fecha: {s_fecha}"
        ])

    # Crear respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="reportes_sobre_pagos_{filtro_seleccionado}.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response




def report_pagos_acreedores(request, filtro_seleccionado, anio, mes, total):
    # Mapeo de filtros válidos
    filtros_validos = {
        'mora_pagada': 'mora_pagada__gt',
        'interes_pagado': 'interes_pagado__gt',
        'aporte_capital': 'aporte_capital__gt',
    }
    filters = Q()
    filters &= Q(fecha__year=anio)
    filters &= Q(fecha__month=mes)
    filters &= Q(pago__registro_ficticio=False)
    filters &= Q(pago__acreedor__isnull=False)

   

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
    sheet.append(["#", "FECHA", "CODIGO DEL ACREEDOR", "NOMBRE DEL ACREEDOR", "NO. REFERENCIA", "MONTO PAGADO", "STATUS DEL ACREEDOR"])

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
        if reporte.pago.acreedor.estado_aportacion:
            mensaje = 'VIGENTE'
        elif reporte.pago.acreedor.estado_aportacion is None:
            mensaje = 'SIN APORTACIONES'
        else:
            mensaje = 'EN ATRASO'

        aportacion = mensaje
        s_fecha = 'VIGENTE' if reporte.pago.acreedor.estados_fechas else 'EN ATRASO'
        sheet.append([
            idx, 
            str(reporte.fecha),
            str(reporte.pago.acreedor.codigo_acreedor),
            str(reporte.pago.acreedor.nombre_acreedor),
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
