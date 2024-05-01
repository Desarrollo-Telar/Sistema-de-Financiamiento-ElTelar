from .send_mail import plantilla_enviar_correo, enviar_correo
from django.shortcuts import render


def prueba(request):
    enviar_correo('Mensaje de prueba', 'Esto solo es una prueba', 'eloicx@gmail.com')