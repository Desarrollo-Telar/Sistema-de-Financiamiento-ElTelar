from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo

# Manejo de mensajes
from django.contrib import messages

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import usuario_activo, usuario_administrador, usuario_contabilidad, usuario_secretaria
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# LIBRERIAS PARA CRUD
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.db.models import Q

### ----------------- LISTAR ------------------------ ###    
from apps.financings.functions import realizar_pago
from apps.financings.functions_payment import generar
from apps.financings.task import comparacion_para_boletas_divididas

## ----------- 
from apps.financings.tareas_ansicronicas import ver_cuotas_no_cargadas
from asgiref.sync import async_to_sync
# TIEMPO
from datetime import datetime
from django.utils.timezone import now


@login_required
@usuario_activo
def list_payment(request):
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(registro_ficticio=False).order_by('-id'))
    ver_cuotas_no_cargadas()
    context = {
        'title':'EL TELAR - PAGOS',
        'page_obj':page_obj,
        'payment_list':page_obj,
        'count':Payment.objects.filter(registro_ficticio=False).count()

        
    }
    return render(request,template_name, context)

@login_required
@usuario_activo
def list_bank(request):
    template_name = 'financings/bank/list.html'
    page_obj = paginacion(request, Banco.objects.filter(registro_ficticio=False).order_by('-fecha'))
    

    context = {
        'title':'EL TELAR - BANCOS',
        'page_obj':page_obj,
        'banco_list':page_obj,
        'count':Banco.objects.filter(registro_ficticio=False).count()
    }
    return render(request,template_name, context)


@login_required
@usuario_activo
def list_credit(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.all().order_by('-id'))
    
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.all().count(),
        'filtro_seleccionado':'Todos',
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_guarantee(request):
    template_name = 'financings/guarantee/lists.html'
    page_obj = paginacion(request, Guarantees.objects.all().order_by('-id'))

    context = {
        'title':'ELTELAR - GARANTIAS',
        'page_obj':page_obj,
        'list_guarantee':page_obj,
        'detalle_garantia':DetailsGuarantees.objects.all(),
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def list_disbursement(request):
    template_name = 'financings/disbursement/list.html'
    page_obj = paginacion(request, Disbursement.objects.all().order_by('-id'))
    context = {
        'title':'ELTELAR - DESEMBOLSOS',
        'page_obj':page_obj,
        'list_disbursement':page_obj
    }
    return render(request, template_name, context)




@login_required
@usuario_activo
def list_clasificacion(request):
    template_name = 'financings/credit/clasificacion.html'
    
    context = {
        'title':'ELTELAR - CLASIFICACION DE CREDITOS',
        'posicion':'Creditos',
        

        
    }
    return render(request, template_name, context)



    
