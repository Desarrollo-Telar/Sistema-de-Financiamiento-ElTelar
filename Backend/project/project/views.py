from .send_mail import plantilla_enviar_correo, enviar_correo


from django.shortcuts import render, redirect, get_object_or_404

# Login
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

# Manejo de mensajes
from django.contrib import messages

# Formularios
from apps.codes.forms import CodeForm

# Modelos
from apps.users.models import User
from django.contrib.auth.models import AnonymousUser

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
            
            request.session['pk'] = user.pk
            return redirect('verification')
        else:
            messages.error(request, 'Credenciales no validos, por favor revise si ingreso correctamente su correo electronico o su contraseña')
    

    context = {
        'title': 'Iniciar Sesión',
    }
    
    
    return render(request, template_name, context)


### --- AÁRTADO PARA VERIFICACION DE DOS PASOS --- ###
def verification(request):
    template_name = 'verification/messages.html'
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if isinstance(request.user,AnonymousUser ):
        if pk:
            user = User.objects.get(pk=pk)
            code = user.code
            code_user = f'{user.username}: {user.code}'
            if not request.POST:
                # send sms
                print(code_user)
            if form.is_valid():
                num = form.cleaned_data.get('number')

                if str(code)==num:
                    code.save()
                    login(request, user)
                    return redirect('index')
                else:
                    return redirect('login')



        context = {
            'form':CodeForm,
        }
    
    else:
        return redirect('index')
    return render(request, template_name, context)


### --- APARTADO INICIAL DEL PROYECTO --- ###
def index(request):
    template_name = 'index.html'
    context = {
        'title':'EL TELAR'
    }
    return render(request, template_name, context)