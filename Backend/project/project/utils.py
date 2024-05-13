import os

from twilio.rest import Client

def send_verification_code(user_code, phone_numer):
    
    
    
    # Configuración de Twilio
    account_sid = 'AC7e08380ae32b9a350902361188f032ff'
    auth_token = '2615fd4fac76d19b9595c935cf2c10d9'
    client = Client(account_sid, auth_token)

    # Enviar código de verificación por SMS
    """
    message = client.messages.create(
        body=f'Tu código de verificación es: {user_code}',
        from_='+13513004588',
        to='+502{}'.format(phone_numer)
    )
    """ 

    # Enviar código de verificación por WhatsApp
    whatsapp_message = client.messages.create(
        from_='whatsapp:+14155238886',  # Número de teléfono de Twilio en formato de WhatsApp
        body='Tu código de verificación es: ' + user_code,  # Cuerpo del mensaje
        to='whatsapp:+502' + phone_numer  # Número de teléfono del destinatario en formato de WhatsApp
    )


    print('Mensaje enviado... {}'.format(whatsapp_message))