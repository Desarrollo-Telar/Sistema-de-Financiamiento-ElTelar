
from django.shortcuts import render, redirect, get_object_or_404

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

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

# DJANGO HTTP
from django.http import HttpResponse

# QR
import qrcode

#UTILS
from .utils import send_verification_code

# Envio de correos
from .send_mail import send_email_welcome_customer, send_email_code_verification

# Tiempo
import datetime
import calendar

# OS
import os
from django.conf import settings

# Obtener la fecha y hora actual
now = datetime.datetime.now()

def test(request):
    return render(request, 'test/test.html', {
        
    })
    
def prueba(request):
    #send_email_welcome_customer()
    
    return render(request, 'email/send_code.html',{})

### --- GENERACION DE CODIGOS QR --- ###
@login_required
@usuario_activo
def generate_qr(request, data):
    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Agrega los datos al objeto QRCode
    qr.add_data(data)
    qr.make(fit=True)
    # Crea una imagen QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Especifica el directorio y el archivo donde se guardará la imagen QR
    directory = os.path.join(settings.MEDIA_ROOT, 'qr')
    if not os.path.exists(directory):
        os.makedirs(directory)  # Crea el directorio si no existe
    
    filename = f"{data}.png"  # Puedes personalizar el nombre del archivo
    filepath = os.path.join(directory, filename)
    
    # Guarda la imagen QR en el archivo especificado
    img.save(filepath)

    # Guarda la imagen QR en un buffer
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return redirect('customers:customers')

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
        
        if user and user.status:
            
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
                send_email_code_verification(user,code_user)
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
@usuario_activo
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