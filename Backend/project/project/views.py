
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
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
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from django.db.models import Q

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

# PDF
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# SETTINGS OF PROJECT
from django.conf import settings

# CRUD
from django.views.generic import CreateView, View

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


###-- CREACION DE PDFS PARA ALGUN FORMULARIO IVE --###
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources.
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = [os.path.realpath(path) for path in result]
        path = result[0]
    else:
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path



def render_pdf_view(request, id):
    template_path = 'customer/forms/forms_ive.html'
    customer_list = get_object_or_404(Customer, id=id)
    address_list = Address.objects.filter(customer_id=customer_list)
    working_information = WorkingInformation.objects.filter(customer_id=customer_list)
    other_information = OtherSourcesOfIncome.objects.filter(customer_id=customer_list)
    reference = Reference.objects.filter(customer_id=customer_list)
    plan = InvestmentPlan.objects.filter(customer_id=customer_list)

    context = {
        'title': 'EL TELAR - FORMULARIO IVE',
        'customer_list': customer_list,
        'address_list': address_list,  
        'working_information': working_information,
        'other_information': other_information,
        'reference': reference,
        'plan_list': plan,
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FormularioIVE.pdf"'
    
    # Find the template and render it
    template = get_template(template_path)
    html = template.render(context)
    

    # Create a PDF
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
       
    # If error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

    
       

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



