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

from datetime import datetime, timedelta

@login_required
@usuario_activo
def filter_credito_reciente(request):
    template_name = 'financings/credit/list.html'
    hoy = datetime.now()
    inicio = hoy - timedelta(days=5)
    page_obj = paginacion(request, Credit.objects.filter(Q(creation_date__range=[inicio,hoy])).order_by('-id'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(Q(creation_date__range=[inicio,hoy])).count(),
        'filtro_seleccionado':'Recientes'
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_cancelado(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(is_paid_off=True).order_by('-id'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(is_paid_off=True).count(),
        'filtro_seleccionado':'Creditos Cancelados'
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_en_atraso(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(estados_fechas=False).order_by('-fecha_actualizacion'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(estados_fechas=False).count(),
        'filtro_seleccionado':'Creditos en Atraso'
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_con_aportaciones(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(estado_aportacion__isnull=False, is_paid_off=False).order_by('-fecha_actualizacion'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(estado_aportacion__isnull=False, is_paid_off=False).count(),
        'filtro_seleccionado':'Creditos en Atraso'
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_en_falta_aportacion(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(estado_aportacion=False).order_by('-id'))
    
    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(estado_aportacion=False).count(),
        'filtro_seleccionado':'Creditos con falta de Aportacion'
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_con_excedente(request):
    template_name = 'financings/credit/list.html'
    page_obj = paginacion(request, Credit.objects.filter(saldo_actual__lt=0).order_by('-id'))

    

    context = {
        'title':'ELTELAR - CREDITOS',
        'page_obj':page_obj,
        'credit_list':page_obj,
        'count': Credit.objects.filter(saldo_actual__lt=0).count(),
        'filtro_seleccionado': 'Creditos con excedente',
        
    }
    return render(request, template_name, context)

@login_required
@usuario_activo
def filter_credito_por_mes_anio(request):
    template_name = 'financings/credit/list.html'
    

    mes = datetime.now().month
    anio = datetime.now().year

    if request.method == 'POST':
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        

        # Validación de mes y año
        if not mes:
            mes = datetime.now().month
        else:
            mes = int(mes)

        if not anio:
            anio = datetime.now().year
        else:
            anio = int(anio)

    filters = Q()
    filters &= Q(creation_date__year=anio)
    filters &= Q(creation_date__month=mes)
    
    object_list = Credit.objects.filter(filters).order_by('id')
    page_obj = paginacion(request, object_list)
    

    context = {
        'title':'ELTELAR - CREDITOS',
        #'page_obj':page_obj,
        'credit_list':page_obj,
        'reporte':True,
        'reporte_excel':True,
        'reporte_desembolso':True,
        'count': object_list.count(),
        'mes': mes,
        'anio': anio,
        'filtro_seleccionado':'Creditos con falta de Aportacion'
    }
    return render(request, template_name, context)


@login_required
@usuario_activo
def filter_list_payment_pendiente(request):
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(estado_transaccion='PENDIENTE', registro_ficticio=False).order_by('-id'))
    


    context = {
        'title':'EL TELAR - PAGOS',
        'page_obj':page_obj,
        'payment_list':page_obj,
        'count':Payment.objects.filter(estado_transaccion='PENDIENTE', registro_ficticio=False).count()

        
    }
    return render(request,template_name, context)

@login_required
@usuario_activo
def filter_list_payment_completados(request):
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.filter(estado_transaccion='COMPLETADO', registro_ficticio=False).order_by('-id'))
    


    context = {
        'title':'EL TELAR - PAGOS',
        'page_obj':page_obj,
        'payment_list':page_obj,
        'count':Payment.objects.filter(estado_transaccion='COMPLETADO', registro_ficticio=False).count()

        
    }
    return render(request,template_name, context)

@login_required
@usuario_activo
def filter_list_bank_vinculado(request):
    template_name = 'financings/bank/list.html'
    page_obj = paginacion(request, Banco.objects.filter(status=True, registro_ficticio=False).order_by('-fecha'))
    

    context = {
        'title':'EL TELAR - BANCOS',
        'page_obj':page_obj,
        'banco_list':page_obj,
        'count':Banco.objects.filter(status=True, registro_ficticio=False).count()
    }
    return render(request,template_name, context)

@login_required
@usuario_activo
def filter_list_bank_no_vinculado(request):
    template_name = 'financings/bank/list.html'
    page_obj = paginacion(request, Banco.objects.filter(status=False, registro_ficticio=False).order_by('-fecha'))
    

    context = {
        'title':'EL TELAR - BANCOS',
        'page_obj':page_obj,
        'banco_list':page_obj,
        'count':Banco.objects.filter(status=False, registro_ficticio=False).count()
    }
    return render(request,template_name, context)