
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import VerificationToken, User
from twilio.rest import Client


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
    account_sid = 'tu_account_sid_de_twilio'
    auth_token = 'tu_auth_token_de_twilio'
    client = Client(account_sid, auth_token)

    # Enviar código de verificación por SMS
    message = client.messages.create(
        body=f'Tu código de verificación es: {token.code}',
        from_='tu_numero_de_twilio',
        to='numero_del_usuario'
    )

    # Enviar código de verificación por WhatsApp
    whatsapp_message = client.messages.create(
        body=f'Tu código de verificación es: {token.code}',
        from_=f'whatsapp:+502 42249955',
        to=f'whatsapp:+502 {user.telephone}'
    )

    return HttpResponse(f'Se ha enviado el código de verificación al usuario {user.username} por SMS y WhatsApp.')