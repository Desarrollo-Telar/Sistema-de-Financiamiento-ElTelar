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
from apps.financings.models import Credit, PaymentPlan

# Scripts
from scripts.notificaciones.generacion_mensaje_whatsapp import mensaje_cliente_por_credito

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
    print('Manejo de mensajes de whatsaap')

    
    cuota = PaymentPlan.objects.filter(id=491).first()


    link = mensaje_cliente_por_credito('2025-200',491)
    print(link)


  except S3Error as exc:
    print("An error occurred.", exc)