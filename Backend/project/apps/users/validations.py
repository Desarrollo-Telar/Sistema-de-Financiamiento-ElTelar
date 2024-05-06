import re
from django_otp.oath import TOTP
import base64

def validar_correo(correo):
    # Expresión regular básica para validar el formato del correo electrónico
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Lista de dominios conocidos
    dominios_conocidos = ['gmail.com', 'yahoo.com', 'outlook.com']  # Agrega más dominios según sea necesario
    
    # Validar el formato del correo electrónico
    if not re.match(regex, correo):
        return False
    
    # Obtener el dominio del correo electrónico
    dominio = correo.split('@')[-1]
    
    # Verificar si el dominio está en la lista de dominios conocidos
    if dominio not in dominios_conocidos:
        return False
    
    return True

def verificar_codigo(codigo_ingresado, clave_secreta):
    # Crea un objeto TOTP con la clave secreta almacenada
    totp = TOTP(key=clave_secreta, step=300, digits=6)

    # Verifica si el código de verificación ingresado es válido
    if totp.verify(codigo_ingresado):
        return True
    else:
        return False
