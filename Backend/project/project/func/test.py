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

# Scripts
from scripts.notificaciones.generacion_mensaje_whatsapp import mensaje_cliente_por_credito
from scripts.cargar_fiadores.vincular import main_vincular
from scripts.asignar_nuevos_permisos.otorgar_permiso import asignar
from scripts.cargar_estado_cuenta.estado_cuenta import migracion_datos

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



if __name__ == "__main__":
  try:
    #migracion_datos()
    

    dia = datetime.now().date()
    dia_mas_uno = dia + timedelta(days=1)
    creditos = Credit.objects.filter(is_paid_off = False, estado_judicial=False)
    listado_saldo_actual = []
    count = 0



    for credito in creditos:
      print(credito)
      siguiente_pago = PaymentPlan.objects.filter(
          credit_id=credito,
          start_date__lte=dia,
          fecha_limite__gte=dia_mas_uno
      ).first()
      cuotas_vencidas = PaymentPlan.objects.filter(credit_id=credito, cuota_vencida=True).order_by('mes')
      estado_cuenta = AccountStatement.objects.filter(credit=credito).order_by('issue_date')
      #actualizacion(credito)
      if siguiente_pago is None:
          siguiente_pago = PaymentPlan.objects.filter(
          credit_id=credito).order_by('-id').first()
      
      saldo_actual =  siguiente_pago.saldo_pendiente + siguiente_pago.principal
      listado_saldo_actual.append(saldo_actual)

      
    
    for saldos in listado_saldo_actual:
      print(saldos)
      count += saldos
    
    print(count)

    



      
          




  except S3Error as exc:
    print("An error occurred.", exc)