import pywhatkit as kit

# Enviar un mensaje
try:
    kit.sendwhatmsg("+50257525044", "Hola, este es un mensaje automático.", 15, 15)  # Enviar a las 15:30
    print("Mensaje enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar el mensaje: {e}")
