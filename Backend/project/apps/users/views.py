
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import VerificationToken, User
from twilio.rest import Client

from django_otp.oath import TOTP
import base64

#kJp9fd8dcA_4E.d
#QS6XQR9WZYCNVVADUWLBK55D

# Vista para la generacion de codigo
@login_required
def send_verification_code(request):
    user = request.user
    token = VerificationToken.generate_token(user)
    # Aquí puedes enviar el código por correo electrónico, SMS, etc.
    return HttpResponse(f'Se ha enviado el código de verificación al usuario {user.username}.')

@login_required
def send_verification_code(request):
    user = request.user
    token = VerificationToken.generate_token(user)
    
    # Configuración de Twilio
    account_sid = 'US6c813cd6c99c75465ac1fd8557bf236b'
    auth_token = 'QS6XQR9WZYCNVVADUWLBK55D'
    client = Client(account_sid, auth_token)

    # Enviar código de verificación por SMS
    message = client.messages.create(
        body=f'Tu código de verificación es: {token.code}',
        from_='42249955',
        to='numero_del_usuario'
    )

    # Enviar código de verificación por WhatsApp
    whatsapp_message = client.messages.create(
        body=f'Tu código de verificación es: {token.code}',
        from_=f'whatsapp:+502 42249955',
        to='whatsapp:+502 ...'
    )

    return HttpResponse(f'Se ha enviado el código de verificación al usuario {user.username} por SMS y WhatsApp.')



def generar_codigo_secreto():
    # Genera una clave secreta de 16 bytes codificada en base32
    clave_secreta = base64.b32encode(os.urandom(10)).decode('utf-8')

    # Crea un objeto TOTP con la clave secreta y otros parámetros opcionales
    totp = TOTP(key=clave_secreta, step=300, digits=6)

    # Genera y devuelve el código de verificación actual
    codigo_verificacion = totp.token()
    return codigo_verificacion, clave_secreta
