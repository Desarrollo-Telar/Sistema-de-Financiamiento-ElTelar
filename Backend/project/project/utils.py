# system
import os
import json

# Conector
from twilio.rest import Client

# Cargar credenciales
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    raise ValueError("Faltan las credenciales de Twilio en las variables de entorno.")

# Instancia única del cliente
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def mensaje_cliente(destino, mensaje):
    """
    Enviar mensaje por WhatsApp usando una plantilla de Twilio Content.
    :param destino: número sin el +502
    :param mensaje: diccionario con las variables para la plantilla (ej. {"1": "Fecha", "2": "Hora"})
    """
    content_variables_json = json.dumps(mensaje)
 
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
        content_variables=content_variables_json,
        to=f'whatsapp:+502{destino}'
    )

    print("Mensaje enviado. SID:", message.sid)
