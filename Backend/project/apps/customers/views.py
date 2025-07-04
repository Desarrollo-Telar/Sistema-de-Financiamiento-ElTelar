from django.shortcuts import render, get_object_or_404, redirect



# Models
from .models import Customer, CreditCounselor
from apps.addresses.models import Address
from apps.FinancialInformation.models import WorkingInformation, OtherSourcesOfIncome, Reference
from apps.InvestmentPlan.models import InvestmentPlan
from apps.pictures.models import ImagenCustomer
from apps.documents.models import DocumentCustomer
from apps.financings.models import Credit

# LIBRERIAS PARA CRUD

from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido, usuario_activo
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# Formularios
from .forms import CustomerForm, ImmigrationStatus

# MENSAJES
from django.contrib import messages



# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def list_filters(request):
    template_name = 'customer/options.html'
    context = {
        'title':'EL TELAR / REPORTES - CLIENTES',
        'posicion':'Clientes',
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)

# ----- EDITAR INFORMACION PERSONAL DE UN CLIENTE ----- #

@login_required
@permiso_requerido('puede_editar_informacion_personal_cliente')
def update_customer(request, customer_code):
    template_name = 'customer/update.html'
    customer = get_object_or_404(Customer, customer_code=str(customer_code))
        
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers:detail', customer_code=customer.customer_code)
    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'title': f'Actualizacion de Informacion para el cliente. {customer.customer_code}',
        'customer_code': customer.customer_code,
        'permisos':recorrer_los_permisos_usuario(request)
    }
    return render(request, template_name, context)


# ----- ELIMINACION DE CLIENTES ----- #
@login_required
@usuario_activo
def delete_customer(request,id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customers:customers')

@login_required
@permiso_requerido('puede_eliminar_registro_cliente')
def delete_customers(request,id):
    template_name ='customer/delete.html'
    customer = get_object_or_404(Customer, id=id)
    context = {
        'title':f'Eliminar al Cliente. {customer}',
        'customer':customer
    }
    if request.method == 'POST':
        customer.delete()
        messages.success(request,'CLIENTE ELIMINADO')
        return redirect('customers:customers')

    return render(request, template_name, context)

# ----- LISTADO DE CLIENTES ----- #


@login_required
@permiso_requerido('puede_visualizar_el_registro_clientes')
def list_customer(request):
    status = ['Revisión de documentos', 'Aprobado', 'No Aprobado', 'Posible Cliente']
    
    customer_list = Customer.objects.all().order_by('-id').filter(status__in=status)

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()
    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        customer_list = Customer.objects.filter(new_asesor_credito=asesor_autenticado).order_by('-id').filter(status__in=status)

    page_obj = paginacion(request, customer_list)
    template_name = 'customer/list.html'
    context = {
        'title':'Registro de Clientes',
        'page_obj':page_obj,
        'customer_list':page_obj,
        'count':customer_list.count(),
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
    return render(request, template_name, context)

# ----- CREANDO USUARIOS NUEVOS ----- #
@login_required
@permiso_requerido('puede_crear_informacion_personal_cliente')
def add_customer(request):     
    ime = ImmigrationStatus.objects.all()    
    template_name = 'customer/add.html'    
    context = {
        'title': 'Creacion de Clientes',        
        'immigration_status':ime,
        'user_id':request.user.id,
        'accion':'Agregar',
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

# ----- BUSCAR CLIENTES ----- #
class CustomerSearch(ListView):
    template_name = 'customer/list.html'
    paginate_by = 25

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            filters = Q()


            # Definir los filtros utilizando Q objects
            filters |= Q(first_name__icontains=query) 
            filters |= Q(customer_code__icontains=query)
            filters |= Q(last_name__icontains=query)
            filters |= Q(type_identification__icontains=query)
            filters |= Q(gender__icontains=query)

 
            # Filtrar los objetos Customer usando los filtros definidos
            return Customer.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            
            return Customer.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator([permiso_requerido('puede_realizar_consultar_de_clientes')])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = f'Consulta de Clientes. {self.query()}'
        context['count'] = context['customer_list'].count()
        context['posicion'] = self.query() 
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        

        return context

# ----- VER DETALLES DE UN CLIENTE ----- #
@login_required
@permiso_requerido('puede_visualizar_detalle_cliente')
def detail_customer(request,customer_code):
    template_name = 'customer/detail.html'
    
    customer_list = Customer.objects.filter(customer_code=str(customer_code)).first()

    asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

    if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
        customer_list = Customer.objects.filter(customer_code=str(customer_code), new_asesor_credito=asesor_autenticado).first()
        if customer_list is None:
            messages.error(request,'No tienes permitido visualizar el perfil de este cliente.')
            return redirect('customers:customers')


    informacion_laboral = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    otra_informacion_laboral = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    direccion = Address.objects.filter(Q(customer_id=customer_list))
    
    plan_inversion = InvestmentPlan.objects.filter(Q(customer_id=customer_list))
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    imagen = ImagenCustomer.objects.filter(Q(customer_id=customer_list))
    document = DocumentCustomer.objects.filter(Q(customer_id=customer_list))
    credito = Credit.objects.filter(Q(customer_id =customer_list ))

    #print(credito)
      
    

    limite_direccion = False if direccion.count() >= 2 else True

    context = {
        'title': 'Detalle de la Informacion del Cliente. {} {} / {}'.format(customer_list.first_name, customer_list.last_name,str(customer_code)),
        'customer_list':customer_list,
        'user_id':request.user.id,
        'direccion': direccion,  
        'informacion_laboral' :informacion_laboral,
        'laboral':informacion_laboral.exists(),
        'otra':otra_informacion_laboral.exists(),
        'otra_informacion_laboral' :otra_informacion_laboral,
        'reference':reference,
        'plan_inversion':plan_inversion,
        'credit_list':credito,
        'customer_code':customer_code,
        'limite_direccion':limite_direccion,
        'imagen':imagen,
        'document':document,
        'permisos':recorrer_los_permisos_usuario(request),
    }
    return render(request, template_name, context)

# ----- VER FORMULARIO IVE ----- #
def formulario_ive(request, id):
    template_name = 'customer/forms/forms_ive.html'
    customer_list = get_object_or_404(Customer, id=id)
    address_list = Address.objects.filter(Q(customer_id=customer_list))
    working_information = WorkingInformation.objects.filter(Q(customer_id=customer_list))
    other_information = OtherSourcesOfIncome.objects.filter(Q(customer_id=customer_list))
    reference = Reference.objects.filter(Q(customer_id=customer_list))
    plan = InvestmentPlan.objects.filter(Q(customer_id=customer_list)).first()

    context = {
        'title':f'Formulario IVE del Cliente. {customer_list} ',
        'customer_list':customer_list,
        'address_list': address_list,  
        'working_information' :working_information,
        'other_information' :other_information,
        'reference':reference,
        'plan':plan,
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
    return render(request, template_name, context)