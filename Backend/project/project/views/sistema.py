# DECORADORES
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo

# Recoleccion de datos
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.recoleccion_reporte_dashboard import recolectar_informes_status_creditos, recolectar_informacion_cobranza

# OS
import os

# QR
import qrcode

# SETTINGS OF PROJECT
from django.conf import settings

# Modelos
from apps.customers.models import Customer,CreditCounselor, Cobranza
from apps.actividades.models import UserLog


# URLS
from django.shortcuts import render, redirect

# DJANGO HTTP
from django.http import HttpResponse

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


### --- APARTADO INICIAL DEL PROYECTO --- ###

@login_required
@usuario_activo
def index(request):
    template_name = 'index.html'
    clientes = Customer.objects.all()

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
    sucursal = request.session['sucursal_id']

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        clientes = Customer.objects.filter(new_asesor_credito=asesor_autenticado, sucursal=sucursal)

    
    context = {
        'title':'Inicio',
        'clientes':clientes,
        'creditos':recolectar_informes_status_creditos(request),
        'permisos':recorrer_los_permisos_usuario(request),
        'actividad_usuario': UserLog.objects.filter(user=request.user),
        'cobranza':recolectar_informacion_cobranza(asesor_autenticado)
    }
    return render(request, template_name, context)


@login_required
@usuario_activo
def list_reportes_modulos(request):
    template_name = 'reports/clasificacion.html'
    context = {
        'title':'CLASIFICACION DE REPORTES',
        'posicion':'Reportes'
    }
    return render(request, template_name, context)

def agradecimeinto(request):
    template_name = 'notification/agradecimiento.html'
    context = {

    }
    return render(request, template_name, context)