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
from apps.actividades.models import UserLog
from apps.subsidiaries.models import Subsidiary
# Formularios
from apps.codes.forms import CodeForm

# LOGIN
import logging

from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone

from apps.actividades.utils import log_user_action, log_system_event

### -- APARTADO DE SALIR --##
@login_required
def logout_view(request):
    user = request.user

    # Solo ejecutamos la lógica si hay un usuario autenticado
    if user.is_authenticated:
        # Usamos timezone.now() en lugar de datetime.now() para mantener consistencia con zona horaria
        hora = timezone.now()

        # Cierre de sesión (limpia la sesión, elimina cookies y regenera token CSRF)
        logout(request)

        # Notificación por correo / log
        try:
            send_email_user_conect_or_disconect(user, hora, "SALIDO DEL SISTEMA")
        except Exception as e:
            # Evita que un error en el servidor de correo bloquee el flujo del usuario
            
            log_system_event(
                message=f"Error enviando correo de logout para {user}: {e}",
                level_name="ERROR",
                source="LogoutView",
                category_name="Correo"
            )

        messages.success(request, "Sesión cerrada exitosamente")
    else:
        messages.info(request, "No hay una sesión activa para cerrar.")

    return redirect("login")


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

            sucursal = None

            if user.sucursal is not None:
                sucursal = user.sucursal.id
                

            request.session['sucursal_id'] = sucursal
           
            
            messages.success(request,'Bienvenido')
            hora = datetime.now()
            
            try:
                send_email_user_conect_or_disconect(user,hora,'INGRESADO AL SISTEMA')

            except Exception as e:
                log_system_event(
                        message=f"Error enviando correo de login para {user}: {e}",
                        level_name="ERROR",
                        source="LoginView",
                        category_name="Correo"
                )

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