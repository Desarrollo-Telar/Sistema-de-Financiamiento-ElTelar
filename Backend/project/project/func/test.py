from minio import Minio
from minio.error import S3Error

import uuid
import json
import os
import django

# Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # <-- Ajusta si tu settings está en otro path
django.setup()

# Modelos
from apps.customers.models import CreditCounselor, Customer, Cobranza
from apps.financings.models import Credit, PaymentPlan, Banco, Payment, Recibo, AccountStatement, Disbursement
from apps.users.models import User
from apps.subsidiaries.models import Subsidiary

# Scripts
from scripts.notificaciones.generacion_mensaje_whatsapp import mensaje_cliente_por_credito
from scripts.cargar_fiadores.vincular import main_vincular
from scripts.asignar_nuevos_permisos.otorgar_permiso import asignar
from scripts.cargar_estado_cuenta.estado_cuenta import migracion_datos
from scripts.INFILE.fact import guardar_xml_recibo
from scripts.INFILE.consulta_nit import ejemplo_uso_consulta_receptor

# Tiempo
from datetime import datetime, timedelta, timezone
from django.utils import timezone

def main():
  # Create a client for your MinIO server using your access and secret keys
  client = Minio(
    endpoint='pcxl65.stackhero-network.com:443',
    secure=True,
    access_key='WkXu9MHvOHvOsLiJjtda',
    secret_key='g75dCPXZlgogk0KloBAM1BI2SfaqzDp2ufciMrIe'
  )

  # Check if the bucket 'asiatrip' exists, and create it if it does not
  found = client.bucket_exists("asiatrip")
  if not found:
    client.make_bucket("asiatrip")
  else:
    print("Bucket 'asiatrip' already exists")

def xd():
  #asignar()
    # python -m project.func.test
    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    

    # Obtener las primeras cuotas activas por crédito del asesor
    
    creditos = Credit.objects.filter(is_paid_off = False)
   
    print(f'Verificando {creditos.count()} creditos')
    contador = 0

    for credito in creditos:
      cuota = PaymentPlan.objects.filter(
          credit_id=credito,
          start_date__lte=dia,
          fecha_limite__gte=dia_mas_uno
      ).first()
      
      verificacion = cuota.capital_generado - cuota.principal

      if verificacion <= 0:
        contador += 1
        print(cuota)
        cuota.credit_id.estado_aportacion = True
        cuota.credit_id.save()


    print(f'Proceso finalizado. se arreglaron {contador}')


from django.db.models.functions import Replace
from django.db.models import F, Value




def limpiar_nit_de_comas_django_corregido():
    """
    Actualiza el campo 'number_nit' en todos los clientes,
    eliminando todas las comas (',') de la cadena de forma eficiente.
    """
    try:
        # 🎯 USAMOS Value() PARA INDICAR QUE ES UN VALOR LITERAL DE CADENA
        filas_actualizadas = Customer.objects.all().update(
            number_nit=Replace(
                F('number_nit'), 
                Value(','),  # Cadena a buscar: la coma ','
                Value('')   # Cadena de reemplazo: la cadena vacía ''
            )
        )
        
        print(f"✅ Éxito: Se actualizaron {filas_actualizadas} registros.")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar los registros: {e}")
        return False


from django.db import IntegrityError

def limpiar_nit_individualmente_con_manejo_errores():
    """
    Actualiza el campo 'number_nit' uno por uno, manejando errores de 
    clave duplicada para evitar la interrupción del proceso.
    """
    total_registros = Customer.objects.count()
    errores = 0
    actualizados = 0

    # Iterar sobre todos los clientes (usando .iterator() para ser más eficiente en memoria)
    for cliente in Customer.objects.all().iterator():
        
        # Eliminar las comas en Python
        nuevo_nit = cliente.number_nit.replace(',', '')
        
        # Solo intentar guardar si hay un cambio y el nuevo valor no está vacío
        if nuevo_nit != cliente.number_nit and nuevo_nit:
            cliente.number_nit = nuevo_nit
            try:
                cliente.save() # Se realiza una sentencia UPDATE por separado
                actualizados += 1
            
            except IntegrityError as e:
                # Capturamos el error de clave duplicada
                if 'duplicate key value violates unique constraint' in str(e):
                    print(f"⚠️ Omisión: El NIT limpiado '{nuevo_nit}' ya existe en otro registro.")
                    errores += 1
                else:
                    # Otros errores de integridad que queremos ver
                    raise e
            except Exception as e:
                print(f"❌ Error desconocido al guardar cliente {cliente.pk}: {e}")
                errores += 1

    print(f"--- Resumen de la Limpieza ---")
    print(f"Total de registros procesados: {total_registros}")
    print(f"✅ Registros actualizados: {actualizados}")
    print(f"❌ Registros omitidos (duplicados): {errores}")

# Uso:
# limpiar_nit_individualmente_con_manejo_errores()

import re
from django.db import IntegrityError
# Asume que tu modelo se llama 'Customer' y está importado
# from your_app_name.models import Customer 

def limpiar_y_formatear_nit_estandarizado():
    """
    Estandariza el campo 'number_nit' para que solo contenga caracteres 
    alfanuméricos en mayúsculas (ej: 1808964K), manejando errores de duplicidad.
    """
    total_registros = Customer.objects.count()
    errores = 0
    actualizados = 0

    # Iterar sobre todos los clientes (usando .iterator() para mejor rendimiento en memoria)
    for cliente in Customer.objects.all().iterator():
        original_nit = cliente.number_nit
        
        if not original_nit:
            continue
            
        # 1. Limpiar Caracteres No Alfanuméricos
        # r'[^a-zA-Z0-9]' busca cualquier cosa QUE NO sea una letra o un dígito.
        # Esto elimina guiones, comas, puntos, espacios, etc.
        limpio_nit = re.sub(r'[^a-zA-Z0-9]', '', original_nit)
        
        # 2. Formato: Asegurar que esté en mayúsculas
        nuevo_nit = limpio_nit.upper()
        
        # Solo guardar si hubo un cambio y el valor resultante no está vacío
        if nuevo_nit != original_nit and nuevo_nit:
            cliente.number_nit = nuevo_nit
            try:
                # Intenta guardar el cambio en la base de datos
                cliente.save()
                actualizados += 1
            
            except IntegrityError:
                # Captura el error de clave duplicada
                print(f"⚠️ Omisión: El NIT limpio '{nuevo_nit}' ya existe en otro registro. Se ignoró el registro {cliente.pk}.")
                errores += 1
            except Exception as e:
                # Captura cualquier otro error de guardado
                print(f"❌ Error desconocido al guardar cliente {cliente.pk}: {e}")
                errores += 1

    print(f"\n--- Resumen del Proceso de Formateo de NIT ---")
    print(f"Total de registros procesados: {total_registros}")
    print(f"✅ Registros actualizados: {actualizados}")
    print(f"❌ Registros omitidos (duplicados/otros errores): {errores}")

# Uso:
# limpiar_y_formatear_nit_estandarizado()

if __name__ == "__main__":
  try:
    #migracion_datos()
    sucursal = Subsidiary.objects.all().first()
    usuarios_no = ['choc1403','e_bermudez']
    
    for usuario in User.objects.all():
       
       if usuario.username in usuarios_no:
          continue
       
       usuario.sucursal = sucursal
       usuario.save()
    
    

    

    



      
        

  except S3Error as exc:
    print("An error occurred.", exc)