import qrcode
import os

def generate_qr(data, filename):
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

if __name__ == '__main__':
    # Ejemplo de uso
    generate_qr("http://127.0.0.1:8000/customers/detail/2024-1/", "codigoQr_2024-1.png")
    generate_qr("https://github.com/choc1403/e-commerce/blob/master/apps/products/models.py", "codigoQr_2024-N1.png")
    generate_qr("http://127.0.0.1:8000/customers/detail/2024-S1/", "codigoQr_2024-S1.png")
