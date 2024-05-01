from .send_mail import plantilla_enviar_correo, enviar_correo


from django.shortcuts import render, redirect, get_object_or_404

# Login
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

# Manejo de mensajes
from django.contrib import messages

def prueba(request):
    enviar_correo('Mensaje de prueba', 'Esto solo es una prueba', 'eloicx@gmail.com')

### -- APARTADO DE SALIR --##
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

### --- APARTADO PARA INICIAR SESION --- ###
def login_view(request):
    if request.user.is_autenticated:
        return redirect('index')



### --- APARTADO INICIAL DEL PROYECTO --- ###
def index(request):
    template_name = 'index.html'
    context = {
        'title':'EL TELAR'
    }
    return render(request, template_name, context)