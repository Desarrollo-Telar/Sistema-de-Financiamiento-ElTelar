# Modelo
from apps.actividades.models import InformeDiarioSistema, DetalleInformeDiario, ModelHistory
from apps.subsidiaries.models import Subsidiary
from apps.documents.models import DocumentSistema
from apps.users.models import User

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# CONSULTAS
from django.db.models import Q

# TIEMPO
from datetime import datetime, time, timedelta
from django.utils.timezone import now
import time

# FUNCIONES
from .informacion_relacionado_cliente import generando_informacion_cliente, obtener_informacion_creditos_sucursal
from .informacion_relacionada_bancos import generar_informacion_bancos, generar_informacion_recibos, generar_informacion_pagos, generar_informacion_facturas
from .informacion_relacionado_contable import generar_informacion_acreedores, generar_informacion_seguros, generar_informacion_ingresos, generar_informacion_egresos


from django.db import transaction
import asyncio

import os
import subprocess
import zipfile
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


from project.func.rutas import commands


async def info_clientes(sucursal, dia):
    info = await generando_informacion_cliente(sucursal, dia)
    return info

def generando_informe_cierre_diario(dia=None):
    if dia is None:
        dia = datetime.now().date()

    inicio = time.perf_counter()  # ⏱️ Marca el inicio

    log_system_event(
        'Generando el cierre diario',
        'INFO',
        'Sistema',
        'General'
    )

    informes_generados = 0

    with transaction.atomic():
        for sucursal in Subsidiary.objects.all().order_by('id'):
            informe, creado = InformeDiarioSistema.objects.get_or_create(
                fecha_registro=dia,
                sucursal=sucursal
            )

            data_map = {
                'clientes': asyncio.run(info_clientes(sucursal, dia)) ,
                'creditos': asyncio.run(obtener_informacion_creditos_sucursal(sucursal, dia)),
                'bancos': generar_informacion_bancos(sucursal),
                'recibos': generar_informacion_recibos(sucursal),
                'pagos': generar_informacion_pagos(sucursal),
                'facturas': generar_informacion_facturas(sucursal),
                'acreedores': generar_informacion_acreedores(sucursal),
                'seguros': generar_informacion_seguros(sucursal),
                'ingresos': generar_informacion_ingresos(sucursal),
                'egresos': generar_informacion_egresos(sucursal),
            }

            # Crear los detalles del informe
            for key, value in data_map.items():
                DetalleInformeDiario.objects.create(
                    reporte=informe,
                    data={key: value},
                    tipo_datos = key,
                    cantidad = len(value)
                )

            informes_generados += 1

    log_system_event(
        f'Cierre diario generado correctamente ({informes_generados} sucursales procesadas)',
        'SUCCESS',
        'Sistema',
        'General'
    )
    fin = time.perf_counter()  # ⏱️ Marca el final
    duracion = fin - inicio
    print(f"⏳ Tiempo total de ejecución: {duracion:.2f} segundos")

    return f'Cierre diario completado para {informes_generados} sucursales ({dia})'






def generando_copias_de_seguridad(dia=None):
    if dia is None:
        dia = datetime.now().date()

    base_dir = os.path.join(settings.BASE_DIR, "modelos", "fixtures")
    os.makedirs(base_dir, exist_ok=True)
    
    usuarios_email = [user.email for user in User.objects.filter(Q(rol__role_name='Programador'), status=True)]

    print("🧩 Generando archivos JSON...")

    # ✅ Lista de comandos a ejecutar (dumpdata)
   
    # 1️⃣ Ejecutar los dumpdata y validar resultados
    for cmd in commands:
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ Ejecutado: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error ejecutando {cmd}: {e.stderr}")

    # 2️⃣ Crear archivo ZIP
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = os.path.join(base_dir, f"Respaldo_Modelos_{fecha_str}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_name in os.listdir(base_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(base_dir, file_name)
                zipf.write(file_path, arcname=file_name)

    print(f"📦 Archivo ZIP generado: {zip_path}")

    # 3️⃣ Registrar en la base de datos
    try:
        DocumentSistema.objects.create(
            description=f"REPORTE DE RESPALDO DEL {dia.strftime('%d-%m-%Y')}",
            document=zip_path
        )
        print("🗂️ Registro guardado en DocumentSistema.")
    except Exception as e:
        print(f"⚠️ No se pudo registrar el documento en la BD: {e}")

    # 4️⃣ Preparar correo
    asunto = f"Respaldo de modelos JSON ({fecha_str})"
    cuerpo = (
        "Adjunto encontrarás un archivo ZIP con los respaldos de los modelos "
        "exportados en formato JSON."
    )

    mensaje = EmailMultiAlternatives(
        subject=asunto,
        body=cuerpo,
        from_email=settings.EMAIL_HOST_USER,
        to=usuarios_email,
    )

    # 5️⃣ Adjuntar ZIP y enviar
    try:
        with open(zip_path, "rb") as f:
            mensaje.attach(os.path.basename(zip_path), f.read(), "application/zip")

        mensaje.send(fail_silently=False)
        print(f"✅ Correo enviado correctamente a {usuarios_email}.")
    except Exception as e:
        print(f"⚠️ Error al enviar correo: {e}")
