
from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.financings.models import Credit, Guarantees, Disbursement,DetailsGuarantees, Banco, Payment, PaymentPlan, AccountStatement, Recibo
from apps.customers.models import CreditCounselor

# Decoradores
from project.decorador import usuario_activo, permiso_requerido
from django.utils.decorators import method_decorator



# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Manejo de mensajes
from django.contrib import messages

# Tiempo
from datetime import datetime, timedelta

class DesembolsoList(ListView):

    template_name = 'financings/disbursement/list.html'
    
    paginate_by = 75
    def get_queryset(self):
        try:
            request = self.request
            

            # Asignar la consulta a una variable local
            sucursal = self.request.session['sucursal_id']

            query = self.query()

            mes = self.query_mes()
            anio = self.query_anio()

            asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

            # Crear una lista para almacenar los filtros
            filters = Q()

            
            
            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(credit_id__fecha_inicio__icontains=query)
                filters |= Q(credit_id__fecha_vencimiento__icontains=query)
                filters |= Q(credit_id__tipo_credito__icontains=query)
                filters |= Q(credit_id__proposito__icontains=query)
                filters |= Q(credit_id__tipo_credito__icontains=query)
                filters |= Q(credit_id__forma_de_pago__icontains=query)
                filters |= Q(credit_id__codigo_credito__icontains=query)
                filters |= Q(credit_id__customer_id__customer_code__icontains=query)
                filters |= Q(credit_id__customer_id__first_name__icontains=query)
                filters |= Q(credit_id__customer_id__last_name__icontains=query)


                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(credit_id__monto__exact=query)
                    filters |= Q(credit_id__plazo__exact=query)
                    filters |= Q(credit_id__tasa_interes__exact=query)
            
           

            
            if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
                filters &= Q(credit_id__asesor_de_credito=asesor_autenticado)
            
            if anio:
                filters &= Q(credit_id__creation_date__year=anio)
            
            if mes:
                filters &= Q(credit_id__creation_date__month=mes)
            
            if sucursal:
                filters &= Q(credit_id__sucursal=sucursal)

            

            # Filtrar los objetos Banco usando los filtros definidos
            return Disbursement.objects.filter(filters).order_by('-id')
        
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Disbursement.objects.none()

    def query(self):
        return self.request.GET.get('q')
    
    
    def query_mes(self):
        return self.request.GET.get('mes')
    
    def query_anio(self):
        return self.request.GET.get('anio')
    
    @method_decorator(permiso_requerido('puede_ver_registros_credito'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dia = datetime.now().date()

        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')

        
        context['title'] = f'Consulta de Registro Desembolsos de Creditos.'
        context['count'] = context['object_list'].count()
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        
        context['list_disbursement'] = context['object_list']
        context['posicion'] = self.query() if self.query() else ''        
        context['query'] = self.query() if self.query() else ''
        
        context['mes'] = int(self.query_mes()) if self.query_mes() else str(dia.month)
        context['anio'] = int(self.query_anio()) if self.query_anio() else str(dia.year)
        return context
