
# ...abs
from django.shortcuts import render, get_object_or_404, redirect

# Paginacion
from project.pagination import paginacion

# Tiempo
from datetime import datetime

# Modelos
from apps.financings.models import Recibo

# Manejo de mensajes
from django.contrib import messages

# Manejador de filtros
from django.db.models import Q
from django.db.models import Q, Sum

# REPORTE EXCEL
from project.reports_excel import report_pagos
from apps.financings.models import Banco, Payment
from openpyxl import Workbook
from django.http import HttpResponse

from apps.financings.formato import formatear_numero

from project.reports_excel import report_pagos

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
    filters &= Q(pago__registro_ficticio=False)
    filters &= Q(pago__credit__isnull=False)

    # Filtro dinámico según selección del usuario
    filtros_validos = {
        'mora_pagada': 'mora_pagada__gt',
        'interes_pagado': 'interes_pagado__gt',
        'aporte_capital': 'aporte_capital__gt',
        'banco':'banco',
    }
    reportes = None
    if filtro_seleccionado in filtros_validos:
        filtro_dinamico = {filtros_validos[filtro_seleccionado]: 0}
        if filtro_seleccionado != 'banco':
            reportes = Recibo.objects.filter(filters).filter(**filtro_dinamico)
            for reporte in reportes:
                if filtro_seleccionado == 'mora_pagada':
                    total += reporte.mora_pagada
                elif filtro_seleccionado == 'interes_pagado':
                    total += reporte.interes_pagado
                else:
                    total += reporte.aporte_capital
            
            
        else:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Reporte de Bancos"

            # Agregar encabezados
            sheet['A1'] = "STATUS"
            sheet['B1'] = "FECHA"
            sheet['C1'] = "DESCRIPCION"
            sheet['D1'] = "REFERENCIA"
            sheet['E1'] = "SECUENCIAL"
            sheet['F1'] = "CHEQUE PROPIO/LOCAL/EFECTIVO"
            sheet['G1'] = "DEBITO(-)"
            sheet['H1'] = "CREDITO(+)"
            sheet['I1'] = "SALDO CONTABLE"
            sheet['J1'] = "SALDO DISPONIBLE"
            sheet['L1'] = "MONTO REF COMPARATIVA"
            sheet['M1'] = "TIPO DE PAGO"
            sheet['N1'] = "DESCRIPCION"
            sheet['O1'] = "FECHA"
            sheet['P1'] = "PARA"

            # Obtener datos de la base de datos, ordenando por status (True primero)
            bancos = Banco.objects.filter(filters).order_by('-status')  # True primero, luego False

            # Agregar datos al archivo
            for idx, banco in enumerate(bancos, start=2):  # Comenzar en la fila 2
                numero_referencia = banco.referencia

                # Buscar el objeto Payment asociado
                boleta = Payment.objects.filter(numero_referencia=numero_referencia).first()

                sheet[f'A{idx}'] = banco.status
                sheet[f'B{idx}'] = banco.fecha
                sheet[f'C{idx}'] = banco.descripcion
                sheet[f'D{idx}'] = banco.referencia
                sheet[f'E{idx}'] = banco.secuencial
                sheet[f'F{idx}'] = banco.cheque
                sheet[f'G{idx}'] = banco.debito
                sheet[f'H{idx}'] = banco.credito
                sheet[f'I{idx}'] = banco.saldo_contable
                sheet[f'J{idx}'] = banco.saldo_disponible

                # Agregar datos de boleta si existe
                if boleta:
                    sheet[f'L{idx}'] = boleta.monto
                    sheet[f'M{idx}'] = boleta.tipo_pago
                    sheet[f'N{idx}'] = boleta.descripcion
                    sheet[f'O{idx}'] = boleta.fecha_emision.date()
                    if boleta.acreedor:
                        sheet[f'P{idx}'] = str(boleta.acreedor)
                    if boleta.seguro:
                        sheet[f'P{idx}'] = str(boleta.seguro)
                    if boleta.cliente:
                        sheet[f'P{idx}'] = str(boleta.cliente)
                    if boleta.credit:
                        sheet[f'P{idx}'] = str(boleta.credit)
                        
                    if boleta.disbursement:
                        sheet[f'P{idx}'] = str(boleta.disbursement)




            # Crear respuesta HTTP para descargar el archivo
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename="reporte_bancos.xlsx"'

            # Guardar el archivo en la respuesta
            workbook.save(response)
            return response

            


        

    else:
        return redirect('financings:reportes')

    # Calcular el total del campo seleccionado
    total_seleccionado = 0
    if filtro_seleccionado in filtros_validos:
        if filtro_seleccionado != 'banco':
            total_seleccionado = reportes.aggregate(Sum(filtro_seleccionado))[f'{filtro_seleccionado}__sum'] or 0
    
    to = formatear_numero(total_seleccionado)

    context = {
        'title': 'ElTELAR',
        'posicion': filtro_seleccionado,
        'reportes': reportes,
        'filters':filters,
        'mes': mes,
        'anio': anio,
        'filtro_seleccionado': filtro_seleccionado,
        'total_seleccionado': to,
        'total':formatear_numero(total)
    }
    return render(request, template_name, context)

