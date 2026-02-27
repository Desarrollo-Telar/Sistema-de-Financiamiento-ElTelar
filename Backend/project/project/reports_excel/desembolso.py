from apps.financings.models import Credit, PaymentPlan, Disbursement, Payment, Guarantees
from apps.FinancialInformation.models import WorkingInformation
from apps.subsidiaries.models import Subsidiary
from apps.customers.models import CreditCounselor
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

from django.db.models import Q
from django.views.generic import TemplateView
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime

class ReporteDesembolsos(TemplateView):
    def get_queryset(self):
        try:
            request = self.request
            sucursal_id = request.session.get('sucursal_id')
            mes = self.query_mes()
            anio = self.query_anio()

            # Base del filtro: Sucursal
            filters = Q(credit_id__sucursal_id=sucursal_id)

            # Filtros dinámicos de Mes y Año
            if anio:
                filters &= Q(credit_id__creation_date__year=anio)
            if mes:
                filters &= Q(credit_id__creation_date__month=mes)

            # Si el usuario es Asesor, filtrar solo sus desembolsos
            asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
            if asesor_autenticado and request.user.rol.role_name == 'Asesor de Crédito':
                filters &= Q(credit_id__asesor_de_credito=asesor_autenticado)

            return Disbursement.objects.filter(filters).order_by('id')
        
        except Exception as e:
            print(f"Error en queryset desembolsos: {e}")
            return Disbursement.objects.none()

    def query_mes(self):
        return self.request.GET.get('mes')

    def query_anio(self):
        return self.request.GET.get('anio')

    def get(self, request, *args, **kwargs):
        # Generación del Excel
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "REPORTE SOBRE DESEMBOLSOS"

        # Encabezados
        sheet.append([
            "#", "CODIGO DEL CLIENTE", "NOMBRE", 
            "FECHA DE DESMBOLSO", "FECHA DE VENCIMIENTO", "FECHA DE CREACION","TASA", 
            "FORMA DE OTORGAMIENTO", "REFERENCIA DE DESEMBOLSO",
            "FORMA DE PAGO", "PLAZO", "TIPO DE GARANTIA","TELEFONO 1", 
            "TELEFONO 2", "LUGAR DE TRABAJO / NEGOCIO", 
            "ASESOR DE CREDITO", "TIPO DE CREDITO", "PROPOSITO","FECHA DE REGISTRO", 
            "MONTO OTORGADO","MONTO DESEMBOLSADO","SALDO ANTERIOR DEL CREDITO", 
            "GASTOS ADMINISTRATIVOS", "MONTO DEL SEGURO", "SALDO PENDIENTE DE DESEMBOLSO", 
            "TIPO DE DESEMBOLSO", "SUCURSAL"
        ])

        reportes = self.get_queryset()

        for idx, reporte in enumerate(reportes, start=1):
            # Lógica de búsqueda de objetos relacionados (idéntica a tu función anterior)
            boleta_desembolso = Payment.objects.filter(
                monto=reporte.monto_desembolsado, 
                disbursement=reporte.id
            ).first()
            
            garantia = Guarantees.objects.filter(credit_id=reporte.credit_id.id).first()
            
            informacion_laboral = WorkingInformation.objects.filter(
                customer_id=reporte.credit_id.customer_id.id
            ).first()

            sheet.append([
                idx,
                str(reporte.credit_id.customer_id.customer_code),
                str(reporte.credit_id.customer_id.get_full_name()),
                str(reporte.credit_id.fecha_inicio),
                str(reporte.credit_id.fecha_vencimiento),
                str(reporte.credit_id.creation_date.date()),
                str(reporte.credit_id.tasa_mensual()),
                '---',
                str(boleta_desembolso.numero_referencia if boleta_desembolso else '---'),
                str(reporte.credit_id.forma_de_pago),
                str(reporte.credit_id.plazo),
                str(garantia.tipos_garantia() if garantia else '---'),
                str(reporte.credit_id.customer_id.telephone),
                str(reporte.credit_id.customer_id.other_telephone or '---'),
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

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Nombre de archivo dinámico según filtros
        mes = self.query_mes() or "todos"
        anio = self.query_anio() or "todos"
        response['Content-Disposition'] = f'attachment; filename="desembolsos_{mes}_{anio}.xlsx"'
        
        workbook.save(response)
        return response