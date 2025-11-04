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
from scripts.cierre_diarrio.generar_cierre_diario import generando_copias_de_seguridad, generar_informacion_facturas, Subsidiary, DetalleInformeDiario
import asyncio
import time
from asgiref.sync import sync_to_async

# pruebas de excel
from project.reports_excel.cierre_diario.cierre_creditos import crear_excel_creditos

# Modelos
from apps.financings.models import Credit, AccountStatement, Payment
from django.db.models import Q


@sync_to_async
def obtener_primera_sucursal():
    return Subsidiary.objects.all().order_by('id').first()


async def main():
    inicio = time.perf_counter()  # ⏱️ Marca el inicio

    sucursal = await obtener_primera_sucursal()

    if not sucursal:
        print("No hay sucursales registradas.")
        return

    print(f"✅ Procesando información de la sucursal: {sucursal.nombre}")

    info = await generando_informacion_cliente(sucursal)

    print(f"🔍 Total clientes procesados: {len(info)}")

    if info:
        print(info[0])

    fin = time.perf_counter()  # ⏱️ Marca el final
    duracion = fin - inicio
    print(f"⏳ Tiempo total de ejecución: {duracion:.2f} segundos")


if __name__ == '__main__':
    generando_copias_de_seguridad()


        

    
    
    

    