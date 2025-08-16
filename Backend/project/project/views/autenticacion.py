
# Decoradores
from django.contrib.auth.decorators import login_required

# Manejo de mensajes
from django.contrib import messages

# Login
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate

# URL
from django.shortcuts import render, redirect


# Envio de correos
from project.send_mail import send_email_code_verification, send_email_user_conect_or_disconect

# Tiempo
from datetime import datetime

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan

# MODELOS
from django.contrib.auth.models import AnonymousUser
from apps.users.models import User
# Formularios
from apps.codes.forms import CodeForm

# LOGIN
import logging

### -- APARTADO DE SALIR --##
@login_required
def logout_view(request):
    user = request.user
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    hora = datetime.now()
    
    send_email_user_conect_or_disconect(user,hora,'SALIDO DEL SISTEMA')
    return redirect('login')


### --- APARTADO PARA INICIAR SESION --- ###
def login_view(request):
    template_name = 'user/login.html'
    cambiar_plan() # CAMBIAR AUTOMATICAMENTE PARA PRUEBAS
    
    # Verificar que no este autenticado
    if request.user.is_authenticated:
        return redirect('index')
    
    # Registro de credenciales
    if request.method == 'POST':
        
        username = request.POST.get('username')  # diccionario
        password = request.POST.get('password')  # None
        

        user = authenticate(username=username, password=password)  # None
        
        if user and user.status:
            
            request.session['pk'] = user.pk
            login(request, user)
            messages.success(request,'Bienvenido')
            hora = datetime.now()
            if user.username != 'choc1403':
                send_email_user_conect_or_disconect(user,hora,'INGRESADO AL SISTEMA')

            next_url = request.GET.get('next') or request.POST.get('next')

            if next_url:
                return redirect(next_url)
            
            return redirect('index')
        else:
            messages.error(request, 'Credenciales no validos')
    

    context = {
        'title': 'Iniciar Sesión',
    }
    
    
    return render(request, template_name, context)

### --- AÁRTADO PARA VERIFICACION DE DOS PASOS --- ###
def verification(request):
    template_name = 'verification/messages.html'
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if isinstance(request.user,AnonymousUser ):
        if pk:
            user = User.objects.get(pk=pk)
            code = user.code
            code_user = f'{user.username}: {user.code}'
            if not request.POST:
                # send sms
                #print(code_user)
                logging.info(code_user)
                send_email_code_verification(user,code_user)
                
            if form.is_valid():
                num = form.cleaned_data.get('number')

                if str(code)==num:
                    code.save()
                    login(request, user)
                    #messages.success(request, 'Credenciales validos. ¡Bienvenido!')
                    return redirect('index')
                else:
                    return redirect('login')



        context = {
            'form':CodeForm,
        }
    
    else:
        return redirect('index')
    return render(request, template_name, context)