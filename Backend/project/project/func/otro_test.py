import os
import django

# Configura el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now

from scripts.cierre_diarrio.informacion_relacionado_cliente import generando_informacion_cliente
from scripts.manejo_excedentes.recalcular import cuotas_con_excedente
from scripts.cierre_diarrio.generar_cierre_diario import  generar_cierre_diario_seguro, ejecutar_cierre_diario, generar_cierre_diario
from scripts.INFILE.consulta_nit import consulta_receptor

from apps.customers.models import CreditCounselor, Cobranza, Customer
from apps.financings.models import Credit, PaymentPlan, Recibo
from apps.actividades.models import Informe, DetalleInformeCobranza, ModelHistory, DetalleInformeDiario


from datetime import date
from scripts.conversion_datos import model_to_dict, cambios_realizados
from django.apps import apps
from apps.subsidiaries.models import Subsidiary
import uuid
from django.db.models import Q

def pruebas(dia, sucursal):
   from django.db import connection

   with connection.cursor() as cursor:
      cursor.execute("CALL generar_informe_diario(%s, %s)", [dia, sucursal.id])



def cuota(creditos):
   dia = datetime.now().date()
   dia_mas_uno = dia + timedelta(days=1)
   cuota_actual = None
   saldo_capital = 0
   informacion_actual = {}

   for credito in creditos:
      cuota_actual = PaymentPlan.objects.filter(
         credit_id=credito,
         start_date__lte=dia,
         fecha_limite__gte=dia_mas_uno
      ).first()

      if cuota_actual is not None:
        saldo_capital += cuota_actual.saldo_pendiente
        credito.saldo_pendiente = cuota_actual.saldo_pendiente
        credito.save()


   informacion_actual['saldo_capital'] = saldo_capital
    
   

   return saldo_capital

from django.db.models import Sum, OuterRef, Subquery, Q, DecimalField, Case, When
from django.db.models.functions import Coalesce
from django.db.models import Sum, OuterRef, Subquery, Q, DecimalField
from django.db.models.functions import Coalesce

from django.db.models import Sum, Q, DecimalField, Case, When
from django.db.models.functions import Coalesce

def obtener_cartera_por_asesor(sucursal_id):
    # 1. Definimos los filtros de créditos "limpios" (sin procesos judiciales)
    filtros_limpios = Q(
        sucursal_id=sucursal_id,
        is_paid_off=False,
        estado_judicial=False,
        categoria_credito_demandado__isnull=True
    )

    # 2. Consulta agrupada por asesor usando el campo saldo_pendiente de Credit
    data = (
        Credit.objects.filter(filtros_limpios)
        .values('asesor_de_credito__nombre', 'asesor_de_credito__apellido')
        .annotate(
            # Sumamos directamente el campo del modelo Credit
            saldo_cartera_total=Coalesce(
                Sum('saldo_pendiente'), 
                0, 
                output_field=DecimalField()
            ),
            # Sumamos el saldo_pendiente solo si el crédito está en atraso
            saldo_en_atraso=Coalesce(
                Sum(
                    Case(
                        When(estados_fechas=False, then='saldo_pendiente'),
                        default=0,
                        output_field=DecimalField()
                    )
                ),
                0, 
                output_field=DecimalField()
            )
        )
        .order_by('-saldo_cartera_total')
    )
    
    return data

from apps.financings.models import Credit, PaymentPlan, Disbursement, Payment, Guarantees
from apps.FinancialInformation.models import WorkingInformation
from apps.subsidiaries.models import Subsidiary
from openpyxl import Workbook
from django.http import HttpResponse



import json
from django.http import HttpResponse
from django.db.models import Q, Sum
from datetime import datetime, timedelta

def report_desmbolso( anio):
    filters = Q()
    filters &= Q(credit_id__creation_date__year=anio)
    
    
    sucursal = Subsidiary.objects.get(id=1)
    

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
    response['Content-Disposition'] = f'attachment; filename="reportes_sobre_desembolsos__{anio}.xlsx"'

    # Guardar el archivo en la respuesta
    workbook.save(response)
    return response

def cobran():
    

    # 1. Obtenemos los IDs de las cuotas desde la tabla de recibos (el Subquery)
    cuotas_ids = Recibo.objects.values_list('cuota', flat=True)

    # 2. Ejecutamos el update masivo
    Cobranza.objects.filter(
        estado_cobranza__in=['PENDIENTE', 'INCUMPLIDO'],
        cuota__in=cuotas_ids
    ).update(
        estado_cobranza='COMPLETADO',
        resultado='Pago realizado'
    )

if __name__ == '__main__':
   report_desmbolso(2025)
   
   
  

  
