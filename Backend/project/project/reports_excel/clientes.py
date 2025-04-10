from apps.financings.models import Credit, PaymentPlan, Disbursement
from apps.customers.models import Customer
from openpyxl import Workbook
from django.http import HttpResponse



import json
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q, Sum
from datetime import datetime, timedelta

def report_clientes(request, filtro_seleccionado):
    hoy = datetime.now()
    inicio = hoy - timedelta(days=5)

    # Diccionario de filtros
    filtros = {
        'Todos': lambda: Credit.objects.all(),
        'Recientes': lambda: Credit.objects.filter(creation_date__range=[inicio, hoy]),
        'Creditos Cancelados': lambda: Credit.objects.filter(is_paid_off=True),
        'Creditos en Atraso': lambda: Credit.objects.filter(estados_fechas=False),
        'Creditos con falta de Aportacion': lambda: Credit.objects.filter(estado_aportacion=False),
        'Creditos con excedente': lambda: Credit.objects.filter(saldo_actual__lt=0),
    }

    # Obtener los créditos según el filtro seleccionado
    reportes = filtros.get(filtro_seleccionado, lambda: Credit.objects.none())().order_by('-id')
    
    # Crear el archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"Reporte de CREDITOS"

    # Agregar encabezado
    sheet['A1'] = f'REPORTE SOBRE CREDITOS'
    sheet.append([
        "#", "FECHA DE REGISTRO", "CODIGO DEL CREDITO", 
        "CLIENTE", "MONTO OTORGADO", "PROPOSITO", "PLAZO EN MESES", "TASA DE INTERES",
        "FORMA DE PAGO", "TIPO DE CREDITO", "DESEMBOLSO","FECHA DE INICIO DEL CREDITO", 
        "FECHA DE VENCIMIENTO DEL CREDITO", "FECHA LIMITE DE PAGO", 
        "SALDO ACTUAL", "SALDO CAPITAL PENDIENTE", "STATUS DEL CREDITO"
    ])

    # Agregar los datos
    for idx, reporte in enumerate(reportes, start=1):
        cuota_limite = PaymentPlan.objects.filter(credit_id__id=reporte.id).order_by('-id').first()
        desembolso = Disbursement.objects.filter(credit_id__id=reporte.id).first()
        fecha_limite_pago = cuota_limite.mostrar_fecha_limite().date() if cuota_limite else "---"
        desembolso_forma = desembolso.forma_desembolso if desembolso else "---"

        # Mensajes de estado
        if reporte.estado_aportacion:
            mensaje = 'VIGENTE'
        elif reporte.estado_aportacion is None:
            mensaje = 'SIN APORTACIONES'
        else:
            mensaje = 'EN ATRASO'

        aportacion = mensaje
        s_fecha = 'VIGENTE' if reporte.estados_fechas else 'EN ATRASO'
        stat = f'''Status de Aportación: {aportacion}, Status por Fecha: {s_fecha}'''

        sheet.append([
            idx,
            reporte.creation_date.date(),
            reporte.codigo_credito,
            reporte.customer_id.get_full_name() if reporte.customer_id else "Sin cliente",
            reporte.formato_monto(),
            reporte.proposito,
            reporte.plazo,
            reporte.tasa_mensual(),
            str(reporte.forma_de_pago),
            str(reporte.tipo_credito),
            str(desembolso_forma),
            reporte.fecha_inicio,
            reporte.fecha_vencimiento,
            fecha_limite_pago,
            reporte.formato_saldo_actual(),
            reporte.formato_saldo_pendiente(),
            stat
        ])

    # Crear la respuesta HTTP
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="reportes_sobre_creditos_{filtro_seleccionado}.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response