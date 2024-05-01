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
    template_name = 'user/login.html'
    
    # Verificar que no este autenticado
    if request.user.is_authenticated:
        return redirect('index')
    
    # Registro de credenciales
    if request.method == 'POST':
        
        username = request.POST.get('username')  # diccionario
        password = request.POST.get('password')  # None

        user = authenticate(username=username, password=password)  # None
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciales no validos, por favor revise si ingreso correctamente su correo electronico o su contraseña')
    

    context = {
        'title': 'Iniciar Sesión',
    }
    
    
    return render(request, template_name, context)



### --- APARTADO INICIAL DEL PROYECTO --- ###
def index(request):
    template_name = 'index.html'
    context = {
        'title':'EL TELAR'
    }
    return render(request, template_name, context)