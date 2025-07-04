import os
import qrcode
import io

# ALMACENADOR DE ARCHIVOS
from project.database_store import minio_client

# AJUSTES
from project.settings import SERVIDOR

def generate_qr_not_servidor(data, filename):
    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Agrega los datos al objeto QRCode
    qr.add_data(data)
    qr.make(fit=True)
    # Crea una imagen QR
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Especifica el directorio y el archivo donde se guardará la imagen QR
    directory = 'media/qr'
    
    if not os.path.exists(directory):
        os.makedirs(directory)  # Crea el directorio si no existe
    

    filepath = os.path.join(directory, filename)
    img.save(filepath)
    print(f"QR code saved at {filepath}")

def generate_qr_servidor(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    bucket_name = 'asiatrip'
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    object_name = f"qr/{filename}"

    minio_client.put_object(
        bucket_name,
        object_name,
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type='image/png'
    )

    print(f"QR code uploaded to MinIO bucket '{bucket_name}' at '{object_name}'")

def generate_qr(data,filename):
    if SERVIDOR:
        generate_qr_servidor(data,filename)
    else:
        generate_qr_not_servidor(data,filename)


