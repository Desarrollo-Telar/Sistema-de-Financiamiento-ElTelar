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
    query = 'Luis'

    clientes = Customer.objects.filter(asesor__icontains=query)
    asesor = CreditCounselor.objects.filter(nombre__icontains=query).first()
    
    for cliente in clientes:
      cliente.new_asesor_credito = asesor
      cliente.save()

    print('Completado')

  except S3Error as exc:
    print("An error occurred.", exc)