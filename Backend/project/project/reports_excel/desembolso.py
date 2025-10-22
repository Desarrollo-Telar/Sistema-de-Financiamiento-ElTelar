from apps.financings.models import Credit, PaymentPlan, Disbursement, Payment, Guarantees
from apps.FinancialInformation.models import WorkingInformation
from apps.subsidiaries.models import Subsidiary
from openpyxl import Workbook
from django.http import HttpResponse



import json
from django.http import HttpResponse
from django.db.models import Q, Sum
from datetime import datetime, timedelta

def report_desmbolso(request,  mes, anio):
    filters = Q()
    filters &= Q(credit_id__creation_date__year=anio)
    filters &= Q(credit_id__creation_date__month=mes)
    
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])
    

    # Obtener los créditos según el filtro seleccionado
    reportes = Disbursement.objects.filter(filters, credit_id__sucursal=sucursal).order_by('id')
    
    # Crear el archivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = f"REPORTE SOBRE DESEMBOLSOS"

    # Agregar encabezado
    sheet['A1'] = f'REPORTE DESEMBOLSOS DEL CREDITO'
    sheet.append([
        "#", "CODIGO DEL CLIENTE", "NOMBRE", 
        "FECHA DE DESMBOLSO", "FECHA DE VENCIMIENTO", "FECHA DE CREACION","TASA", "FORMA DE OTORGAMIENTO", "REFERENCIA DE DESEMBOLSO",
        "FORMA DE PAGO", "PLAZO", "TIPO DE GARANTIA","TELEFONO 1", 
        "TELEFONO 2", "LUGAR DE TRABAJO / NEGOCIO", 
        "ASESOR DE CREDITO", "TIPO DE CREDITO", "PROPOSITO","FECHA DE REGISTRO", "MONTO OTORGADO","MONTO DESEMBOLSADO","SALDO ANTERIOR DEL CREDITO", 
        "GASTOS ADMINISTRATIVOS", "MONTO DEL SEGURO", "SALDO PENDIENTE DE DESEMBOLSO", "TIPO DE DESEMBOLSO", "SUCURSAL"
    ])

    # Agregar los datos
    for idx, reporte in enumerate(reportes, start=1):

        boleta_desembolso = Payment.objects.filter(monto=reporte.monto_desembolsado, disbursement=reporte.id).first()
        garantia =  Guarantees.objects.filter(credit_id = reporte.credit_id.id).first()
        informacion_laboral = WorkingInformation.objects.filter(customer_id=reporte.credit_id.customer_id.id).first()

        

        sheet.append([
            idx,
            str(reporte.credit_id.customer_id.customer_code),
            str(reporte.credit_id.customer_id.get_full_name()),
            str(reporte.credit_id.fecha_inicio),
            str(reporte.credit_id.fecha_vencimiento),
            str(reporte.credit_id.creation_date.date()),
            str(reporte.credit_id.tasa_mensual()),
            str('---'),
            str(boleta_desembolso.numero_referencia if boleta_desembolso else '---'),
            str(reporte.credit_id.forma_de_pago),
            str(reporte.credit_id.plazo),
            str(garantia.tipos_garantia() if garantia else '---'),
            str(reporte.credit_id.customer_id.telephone),
            str(reporte.credit_id.customer_id.other_telephone if reporte.credit_id.customer_id.other_telephone else '---'),
            str(informacion_laboral.get_empresa_laburo() if informacion_laboral else '---'),
            str(reporte.credit_id.asesor_de_credito),
            str(reporte.credit_id.tipo_credito),
            str(reporte.credit_id.proposito),
            str(reporte.credit_id.creation_date.date()),
            str(reporte.credit_id.formato_monto()),
            str(reporte.f_monto_desembolsado()),
            str(reporte.f_saldo_anterior()),
            str(reporte.f_honorarios()),
            str(reporte.f_poliza_seguro()),
            str(reporte.f_monto_total_desembolso()),
            str(reporte.forma_desembolso),
            str(reporte.credit_id.sucursal)


        ])

    # Crear la respuesta HTTP
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = f'attachment; filename="reportes_sobre_desembolsos_{mes}_{anio}.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response