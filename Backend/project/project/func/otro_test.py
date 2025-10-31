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

if __name__ == '__main__':
    
    #generando_informe_cierre_diario()
    detalle = DetalleInformeDiario.objects.filter(tipo_datos='creditos').order_by('id').first()
    list_nuevos = []
    dia = datetime.now().date()
    

    for dato in detalle.data['creditos']:
        fecha_completa = dato['credito']['creation_date']
        fecha_dt = datetime.fromisoformat(fecha_completa.replace("Z", "+00:00"))
        fecha_formateada = fecha_dt.date().isoformat()
        print(fecha_formateada)
    
    woork = crear_excel_creditos(detalle.data['creditos'])
    woork.save("reporte_creditos.xlsx")

    