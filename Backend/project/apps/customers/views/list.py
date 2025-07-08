from django.shortcuts import render, get_object_or_404, redirect



# Models
from apps.customers.models import Customer, CreditCounselor


# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# Paginacion
from project.pagination import paginacion




# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

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