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
from scripts.cierre_diarrio.generar_cierre_diario import generando_informe_cierre_diario, generar_informacion_facturas, Subsidiary, DetalleInformeDiario



# pruebas de excel
from project.reports_excel.cierre_diario.cierre_creditos import crear_excel_creditos

# Modelos
from apps.financings.models import Credit, AccountStatement, Payment
from django.db.models import Q

if __name__ == '__main__':

    creditos_en_excedentes = Credit.objects.filter(is_paid_off=True).order_by('-id')

    for credito in creditos_en_excedentes:
        ultimo_estado_cuenta = AccountStatement.objects.filter(credit=credito, description='CANCELACIÓN DE CRÉDITO VIGENTE').order_by('-id').first()

        if ultimo_estado_cuenta is None:
            print(f'Revisar este credito: {credito}')
            continue

        

        if ultimo_estado_cuenta.payment is not None:
            fecha = ultimo_estado_cuenta.payment.fecha_emision.date()
        else:
            fecha = ultimo_estado_cuenta.issue_date
            
        print(f'El credito: {credito} se cancelo el: {fecha}')
        credito.fecha_cancelacion = fecha
        credito.save()
        

    
    
    

    