
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

# TAREA ASINCRONICO
from apps.financings.task import cambiar_plan,cambiar_estado
from apps.financings.tareas_ansicronicas import generar_todas_las_cuotas_credito, generar_todas_las_cuotas_acreedores

# Modelos
from apps.users.models import User
from django.contrib.auth.models import AnonymousUser
from apps.customers.models import Customer
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from django.db.models import Q
from django.db import models  
from apps.financings.models import Recibo
from apps.financings.models import *
from apps.accountings.models import Creditor

# DJANGO HTTP
from django.http import HttpResponse

# QR
import qrcode

#UTILS
from .utils import send_verification_code

# Envio de correos
from .send_mail import send_email_welcome_customer, send_email_code_verification, send_email_user_conect_or_disconect

# Tiempo

import calendar
from datetime import datetime,timedelta

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

# LOGIN
import logging

# APPs
from django.apps import apps

# Obtener la fecha y hora actual


# LIBRERIAS PARA CRUD
from django.views.generic import CreateView, TemplateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q


###-- CREACION DE PDFS PARA ALGUN FORMULARIO IVE --###
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def prueba(request):
    cambiar_plan()

    return redirect('index')




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


from apps.financings.formato import formatear_numero
@usuario_activo
def index(request):
    template_name = 'index.html'
    cambiar_plan()
    #recibos = Recibo.objects.filter(factura=False, pago__registro_ficticio =False)

    context = {
        'title':'EL TELAR',
        #'recibos':recibos,
        'clientes':Customer.objects.all(),
        'creditos':Credit.objects.filter(is_paid_off=False),
        'creditos_atrasados':Credit.objects.filter(estados_fechas=False),
    }
    return render(request, template_name, context)


def test(request):
    template_name  = 'email/alert_message.html'
    protocol = request.scheme
    domain = request.get_host()
    full_url = f"{protocol}://{domain}"
    context = {
        'message':'ESTO ES UN MENSAJE',
        'full_url':full_url,
        'object':request.user,
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_api(request):
    template_name = 'API/list.html'
    context = {
        'title':'ELTELAR - API'

    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def actualizacion_test_api(request):
    template_name = 'API/actualizacion.html'
    context = {
        'title':'ELTELAR - API'

    }
    return render(request, template_name, context)

class Search(TemplateView):
    template_name = 'search.html'
    paginate_by = 25

    # Lista de aplicaciones cuyos modelos no queremos incluir en la búsqueda
    excluded_apps = [
        'auth', 
        'contenttypes', 
        'sessions', 
        'admin',
        'django_celery_beat',
    ]

    def get_queryset(self, model, query):
        """
        Obtiene el queryset filtrado para un modelo dado.
        """
        try:
            # Verificar si el campo es CharField o TextField
            fields = [field.name for field in model._meta.fields if isinstance(field, (models.CharField, models.TextField))]
            if fields:  
                query_filter = Q()
                for field in fields:
                    query_filter |= Q(**{f"{field}__icontains": query})
                return model.objects.filter(query_filter)
            return model.objects.none()  # Si no hay campos de texto
        except Exception as e:
            print(f"Error al filtrar el queryset para el modelo {model}: {e}")
            return model.objects.none()

    def query(self):
        """
        Obtiene el término de búsqueda de los parámetros GET.
        """
        return self.request.GET.get('q')

    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Construye el contexto para la plantilla con los resultados de búsqueda.
        """
        context = super().get_context_data(**kwargs)
        query = self.query()
        results = {}
        count = 0
        
        if query:
            # Obtener todos los modelos registrados en la aplicación
            all_models = apps.get_models()

            for model in all_models:
                # Excluir modelos que pertenezcan a las aplicaciones listadas en excluded_apps
                app_label = model._meta.app_label
                if app_label in self.excluded_apps:
                    continue  # Saltar este modelo

                # Filtrar los resultados para cada modelo
                model_results = self.get_queryset(model, query)
                if model_results.exists():
                    results[model._meta.verbose_name_plural] = model_results
                    count += model_results.count()

        context['query'] = query
        context['results'] = results
        context['count'] = count
        context['title'] = 'ELTELAR - Buscar'
        return context

@login_required
@usuario_activo
def list_reportes_modulos(request):
    template_name = 'reports/clasificacion.html'
    context = {
        'title':'EL TELAR - CLASIFICACION DE REPORTES',
        'posicion':'Reportes'
    }
    return render(request, template_name, context)