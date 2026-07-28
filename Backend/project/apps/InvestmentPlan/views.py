from django.shortcuts import render, get_object_or_404, redirect

# FORMULARIO
from .forms import InvestmentPlanForms
# FORMATO
from apps.financings.formato import formatear_numero

# MODELOS
from apps.customers.models import Customer, CreditCounselor
from .models import InvestmentPlan, ExpedientePlanNotario
from apps.users.models import User
from apps.FinancialInformation.models import Reference, WorkingInformation, OtherSourcesOfIncome
from apps.subsidiaries.models import Subsidiary
from apps.documents.models import DocumentExpediente, DocumentCustomer
from apps.pictures.models import ImagenCustomer

# LIBRERIAS PARA CRUD
from django.contrib import messages

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo
from dateutil.relativedelta import relativedelta
#SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from project.send_mail import send_email_new_customer
from scripts.conversion_datos import model_to_dict
# Create your views here.
from apps.financings.views.creditos.funciones import generar_codigo_seguridad
from django.views.decorators.csrf import ensure_csrf_cookie 

@login_required
@usuario_activo
def create_plan_financiamiento(request, customer_code):
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    cantidad = Reference.objects.filter(customer_id=customer_id)
    template_name = 'InvestmentPlan/create.html'
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
    es_asesor = False

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        es_asesor = True
    
    #num = generar_codigo_seguridad(usuario_regis=request.user, accion='Solicitud de Credito.')
    request.session['codigo_migracion'] = 2026

   
    
    context = {
        'customer_id':customer_id,
        'sucursal': sucursal,
        'customer_code':customer_code,
        'es_asesor':es_asesor,
        'permisos':recorrer_los_permisos_usuario(request),
        'disponibilidad_efectiva': formatear_numero(customer_id.disponibilidad_efectiva()),

    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def delete_plan_financiamiento(request, id,customer_code):
    plan = get_object_or_404(InvestmentPlan, id = id)
    plan.delete()
    return redirect('customers:detail',customer_code)


@login_required
@usuario_activo
def gestion_de_expedientes_notarios(request, id):
    plan = get_object_or_404(InvestmentPlan, id=id)
    customer_code = plan.customer_id.customer_code

    if plan.estado_aprobacion != 'ACEPTADO':
        return redirect('customers:detail',customer_code)

    notarios_lista = plan.notarios or []
    expediente_existente = ExpedientePlanNotario.objects.filter(investment_plan=plan)

    if not notarios_lista and not expediente_existente.exists():
        
        # Manejar el caso cuando no hay notarios asignados
        return redirect('customers:detail',customer_code)

    ids_notarios = [notario.get('id') for notario in notarios_lista if notario.get('id')]

    ids_unicos = set(ids_notarios)

    if len(ids_unicos) == 1:
        # CASO 1: Todos los módulos están asignados al mismo notario (ej. ID 1 y ID 1)
        id_unico = list(ids_unicos)[0]
        try:
            user_notario = User.objects.get(id=id_unico)

            return redirect('investment_plan:subir_archivos', plan.id, user_notario.id)
            
        except User.DoesNotExist:
            pass  # Manejo de error si el usuario no existe en la base de datos

   
    usando_ids_unicos = User.objects.filter(id__in=ids_unicos)

    if not usando_ids_unicos:
        messages.error(request, 'Esta Solicitud De Credito No Tiene Notario.')
        return redirect('investment_plan:lista_expedientes_notarios', expediente_existente.uuid)


    template_name = 'InvestmentPlan/gestion_de_expedientes_notarios.html'
    context = {
        'plan_id': plan.id,
        'permisos': recorrer_los_permisos_usuario(request),
        'sucursales': usando_ids_unicos,
    }
    return render(request, template_name, context)



@login_required
@usuario_activo
@ensure_csrf_cookie
def subir_archivos_expedientes_notarios(request,plan_id,user_id):
  
    template_name = 'InvestmentPlan/expediente.html'

    plan = get_object_or_404(InvestmentPlan, id=plan_id)
    notario = get_object_or_404(User, id=user_id)

   
    expediente_existente, created = ExpedientePlanNotario.objects.get_or_create(investment_plan=plan, notario=notario)


    context = {
        'plan': plan,
        'notario': notario, 
        'expediente_id':expediente_existente.id,
        'permisos': recorrer_los_permisos_usuario(request),
        'codigo': expediente_existente.uuid,
    }
    
    return render(request, template_name, context)

    

def lista_expedientes_notarios(request, uuid):
    
    template_name = 'InvestmentPlan/lista_expedientes_notarios.html'
    expedientes = ExpedientePlanNotario.objects.get(uuid=uuid)

    plan = expedientes.investment_plan
    notarios = plan.listado_de_notarios()
    siguiente_expediente = None
    if notarios:

        siguiente_expediente = ExpedientePlanNotario.objects.filter(
            notario__id__in = notarios, investment_plan = plan

        ).exclude(id=expedientes.id)
    es_autenticado = request.user.is_authenticated

    
    customer_code = plan.customer_id.customer_code

    fiadores_lista = plan.fiador or []
    fiadores = None
    informacion_laboral = None
    imagen = None
    document = None

    if  fiadores_lista:
        ids_fiadores = [fiador.get('id') for fiador in fiadores_lista if fiador.get('id')]
        ids_unicos_fiadores = set(ids_fiadores)
        fiadores = Customer.objects.filter(id__in = ids_unicos_fiadores)
        informacion_laboral = WorkingInformation.objects.filter(customer_id__id__in = ids_unicos_fiadores)
        imagen = ImagenCustomer.objects.filter(customer_id__id__in = ids_unicos_fiadores)
        document = DocumentCustomer.objects.filter(customer_id__id__in = ids_unicos_fiadores)

    cliente = Customer.objects.get(customer_code = customer_code)




    context = {
        'expedientes': expedientes,
        'expediente_id': expedientes.id,
        'documentos':DocumentExpediente.objects.filter(expediente=expedientes),
        'es_autenticado': es_autenticado,
        'permisos': recorrer_los_permisos_usuario(request),
        'plan': plan,
        'customer_code': customer_code,
        'cliente': cliente,
        'fiadores': fiadores,
        'informacion_laboral':informacion_laboral,
        'imagen': imagen,
        'document': document,
        'siguiente_expediente':siguiente_expediente
    }

    return render(request, template_name, context)


@login_required
@usuario_activo
def update_plan_financiamiento(request, id, customer_code):
    num = generar_codigo_seguridad(usuario_regis=request.user, accion='Solicitud de Credito.')
    request.session['codigo_migracion'] = num
    template_name = 'InvestmentPlan/create.html'
    get_plan = get_object_or_404(InvestmentPlan, id=id)
    customer_id = get_object_or_404(Customer, customer_code=customer_code)
    sucursal = Subsidiary.objects.get(id=request.session['sucursal_id'])
    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
    es_asesor = False

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        es_asesor = True

    context = {
        'plan': get_plan,  # <-- AGREGADO: Enviamos el objeto con los datos existentes
        'customer_id': customer_id,
        'cliente': customer_id, # Asegura compatibilidad si usabas cliente.id en el hidden input
        'sucursal': sucursal,
        'customer_code': customer_code,
        'es_asesor':es_asesor,
        'permisos': recorrer_los_permisos_usuario(request),
        'disponibilidad_efectiva': formatear_numero(customer_id.disponibilidad_efectiva()),
    }
    return render(request, template_name, context)