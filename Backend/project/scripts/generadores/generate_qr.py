import os

import qrcode
import io

from minio import Minio



minio_client = Minio(
    "pcxl65.stackhero-network.com",
    access_key="WkXu9MHvOHvOsLiJjtda",
    secret_key="g75dCPXZlgogk0KloBAM1BI2SfaqzDp2ufciMrIe",
    secure=True
)

def generate_qr(data, filename):
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


