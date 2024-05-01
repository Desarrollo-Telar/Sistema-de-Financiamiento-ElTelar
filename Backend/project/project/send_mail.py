from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


_EMAIL_FROM = 'develtelar@gmail.com'

def enviar_correo(asunto,mensaje,dirijido):
    subject = asunto
    message = mensaje
    email_from = _EMAIL_FROM
    recipient_list = [dirijido]

    send_mail(subject, message, email_from, recipient_list)

def plantilla_enviar_correo(asunto, mensaje, dirijido):
    subject = asunto
    email_from = _EMAIL_FROM
    recipient_list = dirijido
    
    # Renderizar el contenido de la plantilla
    html_content = render_to_string('email/welcome_message.html', {'nombre_usuario': 'Juan Carlos Choc'})
    
    # Crear el objeto EmailMultiAlternatives para enviar el correo
    email = EmailMultiAlternatives(subject, 'Cuerpo del correo.', email_from, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()