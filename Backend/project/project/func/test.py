from minio import Minio
from minio.error import S3Error

import uuid
import json



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
    
    print('hola')

  except S3Error as exc:
    print("An error occurred.", exc)