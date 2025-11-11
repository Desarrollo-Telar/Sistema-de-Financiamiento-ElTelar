
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

class CreditoList(ListView):

    template_name = 'financings/credit/list.html'
    
    paginate_by = 75
    def get_queryset(self):
        try:
            request = self.request
            

            # Asignar la consulta a una variable local
            sucursal = self.request.session['sucursal_id']

            query = self.query()
            status = self.status()
            mes = self.query_mes()
            anio = self.query_anio()

            asesor_autenticado = CreditCounselor.objects.filter(usuario=request.user).first()

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
            
            if status:
                match status:
                    case 'Recientes':
                        hoy = datetime.now()
                        inicio = hoy - timedelta(days=5)
                        filters &= Q(creation_date__range=[inicio,hoy])

                    case 'Creditos Cancelados':
                        filters &= Q(is_paid_off=True)

                    case 'Creditos en Atraso':
                        filters &= Q(estados_fechas=False)
                    
                    case 'Creditos Falta de Aportacion':
                        filters &= Q(estado_aportacion=False)

                    case 'Creditos en Estado Juridico':
                        filters &= Q(estado_judicial=True)

                    case 'Creditos con Excedente':
                        filters &= (Q(saldo_actual__lt=0) | Q(excedente__gt=0))

            
            if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
                filters &= Q(asesor_de_credito=asesor_autenticado)
            
            if anio:
                filters &= Q(creation_date__year=anio)
            
            if mes:
                filters &= Q(creation_date__month=mes)
            
            if sucursal:
                filters &= Q(sucursal=sucursal)

            

            # Filtrar los objetos Banco usando los filtros definidos
            return Credit.objects.filter(filters).order_by('-id')
        
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Credit.objects.none()

    def query(self):
        return self.request.GET.get('q')
    
    def status(self):
        return self.request.GET.get('status')
    
    def query_mes(self):
        return self.request.GET.get('mes')
    
    def query_anio(self):
        return self.request.GET.get('anio')
    
    @method_decorator(permiso_requerido('puede_realizar_consultas_informacion_credito'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        
        status = ['Recientes', 'Creditos Cancelados','Creditos en Atraso', 'Creditos Falta de Aportacion', 'Creditos en Estado Juridico',
                  'Creditos con Excedente']
        
        
        
        context['title'] = f'Consulta de Registro de Creditos.'
        context['count'] = context['object_list'].count()
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        
        context['posicion'] = self.query() if self.query() else ''        
        context['query'] = self.query() if self.query() else ''
        context['status'] = status
        context['selected_status'] = self.status() if self.status() else ''
        context['mes'] = int(self.query_mes()) if self.query_mes() else ''
        context['anio'] = int(self.query_anio()) if self.query_anio() else ''
        return context
