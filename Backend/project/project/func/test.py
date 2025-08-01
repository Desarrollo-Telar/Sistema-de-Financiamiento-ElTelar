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
from apps.customers.models import CreditCounselor, Customer
from apps.financings.models import Credit, PaymentPlan, Banco, Payment

# Scripts
from scripts.notificaciones.generacion_mensaje_whatsapp import mensaje_cliente_por_credito
from scripts.cargar_fiadores.vincular import main_vincular
from scripts.asignar_nuevos_permisos.otorgar_permiso import asignar

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




if __name__ == "__main__":
  try:
    #asignar()
    # python -m project.func.test
    pagos_status_true = Payment.objects.filter(estado_transaccion='COMPLETADO').order_by('-id')

    for pago in pagos_status_true:
      banco = Banco.objects.filter(referencia=pago.numero_referencia, status=False).first()
      print(banco)
      if banco is not None:
        banco.status = True
        banco.save()
    print('finalizado')


  except S3Error as exc:
    print("An error occurred.", exc)