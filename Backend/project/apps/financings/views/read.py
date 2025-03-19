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
# TIEMPO
from datetime import datetime
from django.utils.timezone import now
def ver_cuotas_no_cargadas():
    planes = PaymentPlan.objects.filter(fecha_limite__month=3, cuota_vencida = False)

    for cuota in planes:
        cuota_actual = cuota
        if cuota.credit_id is None:
            continue
        
        cuotas = PaymentPlan.objects.filter(credit_id = cuota.credit_id).order_by('fecha_limite')
        encontrada = False
        print('----------')
        print(cuota.credit_id)
        print('----------')
        for cuota_de in cuotas:
            
            print(cuota_de.id)

        
        
def cargar_boletas_estado():
    pagos_estado_completado = Payment.objects.filter(estado_transaccion = "COMPLETADO")
    for pago in pagos_estado_completado:
        boleta = Banco.objects.filter(referencia=pago.numero_referencia).first()
        if boleta :
            

            boleta.status = True
            boleta.save()


@login_required
@usuario_activo
def list_payment(request):
    template_name = 'financings/payment/list.html'
    page_obj = paginacion(request, Payment.objects.all().order_by('-id'))
    #cargar_boletas_estado()
    #generar()
    #comparacion_para_boletas_divididas()
    
    #ver_cuotas_no_cargadas()


    context = {
        'title':'EL TELAR - PAGOS',
        'page_obj':page_obj,
        'payment_list':page_obj

        
    }
    return render(request,template_name, context)

@login_required
@usuario_activo
def list_bank(request):
    template_name = 'financings/bank/list.html'
    page_obj = paginacion(request, Banco.objects.all().order_by('-fecha'))
    #generar()
    #comparacion_para_boletas_divididas()
    #cargar_boletas_estado()

    context = {
        'title':'EL TELAR - BANCOS',
        'page_obj':page_obj,
        'banco_list':page_obj,
        'count':Banco.objects.all().count()
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
        'count': Credit.objects.all().count()
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



# ------------------ BUSCADOR ------------------------------
class BankSearch(ListView):
    template_name = 'financings/bank/list.html'
    paginate_by = 25

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha__icontains=query)
                filters |= Q(referencia__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(credito__exact=query)
                    filters |= Q(debito__exact=query)

            # Filtrar los objetos Banco usando los filtros definidos
            return Banco.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Banco.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = 'ELTELAR - Buscar'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query()
        return context

class PaymentSearch(ListView):
    template_name = 'financings/payment/list.html'
    paginate_by = 25

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha_emision__icontains=query)
                filters |= Q(numero_referencia__icontains=query)
                filters |= Q(estado_transaccion__icontains=query)
                filters |= Q(credit__codigo_credito__icontains=query)
                filters |= Q(tipo_pago__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    #filters |= Q(numero_referencia__exact=query)

            # Filtrar los objetos Banco usando los filtros definidos
            return Payment.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Payment.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = 'ELTELAR - Buscar'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query()
        return context

class CreditSearch(ListView):
    template_name = 'financings/credit/list.html'
    paginate_by = 25

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha_inicio__icontains=query)
                filters |= Q(fecha_vencimiento__icontains=query)
                filters |= Q(tipo_credito__icontains=query)
                filters |= Q(proposito__icontains=query)
                filters |= Q(tipo_credito__icontains=query)
                filters |= Q(forma_de_pago__icontains=query)
                filters |= Q(codigo_credito__icontains=query)
                filters |= Q(customer_id__customer_code__icontains=query)
                filters |= Q(customer_id__first_name__icontains=query)
                filters |= Q(customer_id__last_name__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    filters |= Q(plazo__exact=query)
                    filters |= Q(tasa_interes__exact=query)
                    

            # Filtrar los objetos Banco usando los filtros definidos
            return Credit.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Credit.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(usuario_activo)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = 'ELTELAR - Buscar'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query()
        return context