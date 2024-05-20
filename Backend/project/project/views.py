
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


#UTILS
from .utils import send_verification_code

# Envio de correos
from .send_mail import send_email_welcome_customer, send_email_code_verification

# Tiempo
import datetime
import calendar

# Obtener la fecha y hora actual
now = datetime.datetime.now()

def prueba(request):
    #send_email_welcome_customer()
    
    return render(request, 'email/send_code.html',{})

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
        print(username)
        print(password)

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
                #send_email_code_verification(user,code_user)
                #phone_numer = user.telephone
                #send_verification_code(code_user,phone_numer)
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
    # Obtener el día de la fecha actual
    dia_actual = now.day
    mes_actual = now.month
    # Obtener el nombre del mes usando el módulo calendar
    mes_actual_nombre = calendar.month_name[mes_actual]
    context = {
        'title':'EL TELAR',
        'dia':dia_actual,
        'mes':mes_actual_nombre,
    }
    return render(request, template_name, context)