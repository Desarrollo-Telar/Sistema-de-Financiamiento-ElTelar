from django.shortcuts import render

# Models
from apps.accountings.models import Creditor, Insurance,  Egress, Income

# LIBRERIAS PARA CRUD
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido, usuario_activo
from django.utils.decorators import method_decorator

# Paginacion
from project.pagination import paginacion

# TAREA ASINCRONICO
from apps.financings.tareas_ansicronicas import ver_caso_de_gastos

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# MENSAJES
from django.contrib import messages

# Tiempo
from datetime import datetime, timedelta

# Create your views here.
@login_required
@permiso_requerido('puede_ver_registro_acreedores')
def list_acreedores(request):
    template_name = 'contable/acreedores/list.html'
    sucursal = request.session['sucursal_id']
    acreedores_list = Creditor.objects.filter(sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, acreedores_list)
    context = {
        'title':'Registro de Acreedores',
        'page_obj':page_obj,
        'acreedores_list':page_obj,
        'count':acreedores_list.count(),
        'posicion':'Todos los Acreedores',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

class AcreedoresListView(ListView):
    template_name = 'contable/acreedores/list.html'
    paginate_by = 50

    def get_queryset(self):
        try:
            request = self.request

            sucursal = request.session['sucursal_id']
            # Asignar la consulta a una variable local
            query = self.query()
            status = self.status()
            mes = self.query_mes()
            anio = self.query_anio()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha_inicio__icontains=query)
                filters |= Q(fecha_vencimiento__icontains=query)                
                filters |= Q(nombre_acreedor__icontains=query)                
                filters |= Q(codigo_acreedor__icontains=query)
                filters |= Q(numero_referencia__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    filters |= Q(plazo__exact=query)
                    filters |= Q(tasa__exact=query)
            
            if status:
                match status:
                    case 'Recientes':
                        hoy = datetime.now()
                        inicio = hoy - timedelta(days=5)
                        filters &= Q(creation_date__range=[inicio,hoy])

                    case 'Acreedores Cancelados':
                        filters &= Q(is_paid_off=True)

                    case 'En Atraso por Aportación':
                        filters &= Q(estados_fechas=False)
                    
                    case 'En Atraso por Fechas':
                        filters &= Q(estado_aportacion=False)
                  
                    case 'Acreedores con Excedente':
                        filters &= (Q(saldo_actual__lt=0) | Q(excedente__gt=0))
            if anio:
                filters &= Q(creation_date__year=anio)
            
            if mes:
                filters &= Q(creation_date__month=mes)

            if sucursal:
                filters &= Q(sucursal=sucursal) 
                    

            # Filtrar los objetos Banco usando los filtros definidos
            return Creditor.objects.filter(filters).order_by('-id')
        
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Creditor.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    def status(self):
        return self.request.GET.get('status')
    
    def query_mes(self):
        return self.request.GET.get('mes')
    
    def query_anio(self):
        return self.request.GET.get('anio')
    
    @method_decorator(permiso_requerido('puede_ver_registro_acreedores'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = ['Recientes', 'Acreedores Cancelados','En Atraso por Aportación', 'En Atraso por Fechas', 'Acreedores con Excedente']

        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')

        context['query'] = self.query() if self.query() else ''
        context['title'] = f'Registro de Acreedores'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query() if self.query() else ''

        
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['status'] = status
        context['selected_status'] = self.status() if self.status() else ''
        context['mes'] = int(self.query_mes()) if self.query_mes() else ''
        context['anio'] = int(self.query_anio()) if self.query_anio() else ''
        return context


@login_required
@permiso_requerido('puede_ver_registro_seguros')
def list_seguros(request):
    template_name = 'contable/seguros/list.html'
    sucursal = request.session['sucursal_id']
    object_list = Insurance.objects.filter(sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    context = {
        'title':'Registro de Seguros',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Seguros',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

class SeguroListView(ListView):
    template_name = 'contable/seguros/list.html'
    paginate_by = 50

    def get_queryset(self):
        try:
            request = self.request

            sucursal = request.session['sucursal_id']
            # Asignar la consulta a una variable local
            query = self.query()
            status = self.status()
            mes = self.query_mes()
            anio = self.query_anio()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha_inicio__icontains=query)
                filters |= Q(fecha_vencimiento__icontains=query)                
                filters |= Q(nombre_acreedor__icontains=query)                
                filters |= Q(codigo_acreedor__icontains=query)
                filters |= Q(numero_referencia__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    filters |= Q(plazo__exact=query)
                    filters |= Q(tasa__exact=query)
            
            if status:
                match status:
                    case 'Recientes':
                        hoy = datetime.now()
                        inicio = hoy - timedelta(days=5)
                        filters &= Q(creation_date__range=[inicio,hoy])

                    case 'Seguros Cancelados':
                        filters &= Q(is_paid_off=True)

                    case 'En Atraso por Aportación':
                        filters &= Q(estados_fechas=False)
                    
                    case 'En Atraso por Fechas':
                        filters &= Q(estado_aportacion=False)
                  
                    case 'Seguros con Excedente':
                        filters &= (Q(saldo_actual__lt=0) | Q(excedente__gt=0))
            if anio:
                filters &= Q(creation_date__year=anio)
            
            if mes:
                filters &= Q(creation_date__month=mes)

            if sucursal:
                filters &= Q(sucursal=sucursal) 
                    

            # Filtrar los objetos Banco usando los filtros definidos
            return Insurance.objects.filter(filters).order_by('-id')
        
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Insurance.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    def status(self):
        return self.request.GET.get('status')
    
    def query_mes(self):
        return self.request.GET.get('mes')
    
    def query_anio(self):
        return self.request.GET.get('anio')
    
    @method_decorator(permiso_requerido('puede_ver_registro_seguros'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = ['Recientes', 'Seguros Cancelados','En Atraso por Aportación', 'En Atraso por Fechas', 'Seguros con Excedente']

        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')

        context['query'] = self.query() if self.query() else ''
        context['title'] = f'Registro de Seguros'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query() if self.query() else ''

        
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['status'] = status
        context['selected_status'] = self.status() if self.status() else ''
        context['mes'] = int(self.query_mes()) if self.query_mes() else ''
        context['anio'] = int(self.query_anio()) if self.query_anio() else ''
        return context

@login_required
@permiso_requerido('puede_ver_registro_ingresos')
def list_ingresos(request):
    template_name = 'contable/ingresos/list.html'
    sucursal = request.session['sucursal_id']
    object_list = Income.objects.filter(sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    context = {
        'title':'Registro de Ingresos',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Ingresos',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

class IngresosList(ListView):
    template_name = 'contable/ingresos/list.html'
    model = Income
    paginate_by = 25

    def get_queryset(self):
        try:
            sucursal = self.request.session['sucursal_id']
            query = self.query()
            mes = self.mes_reporte()
            anio = self.anio_reporte()

            filters = Q()

            # Filtro por texto
            if query:
                filters |= Q(fecha__icontains=query)
                filters |= Q(codigo_ingreso__icontains=query)
                filters |= Q(numero_referencia__icontains=query)

                if query.isdigit():
                    filters |= Q(monto__exact=query)

            # Filtro por mes
            if mes:
                filters &= Q(fecha__month=mes)

            # Filtro por año
            if anio:
                filters &= Q(fecha__year=anio)

            return Income.objects.filter(filters, sucursal=sucursal).order_by('-id')
        except Exception as e:
            print(f"Error al filtrar el queryset: {e}")
            return Income.objects.none()

    def query(self):
        return self.request.GET.get('q')
    
    def mes_reporte(self):
        return self.request.GET.get('mes')
    
    def anio_reporte(self):
        return self.request.GET.get('anio')
    
    @method_decorator(permiso_requerido('puede_ver_registro_ingresos'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not context['object_list'] and self.query() is not None:

            messages.error(self.request, 'No se encontró ningún dato')

        # Mantener valores que el usuario eligió en el form
        mes = self.mes_reporte() or datetime.now().month
        anio = self.anio_reporte() or datetime.now().year
        
        consulta = self.query() or ''
        
        
        context['query'] =  consulta
        context['title'] = f"Registro de Ingresos"
        context['count'] = context['object_list'].count()
        context['posicion'] = consulta
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['mes'] = int(mes) if mes else datetime.now().month
        context['anio'] = int(anio) if anio else  datetime.now().year

        return context



@login_required
@permiso_requerido('puede_ver_registro_egresos')
def list_egresos(request):
    sucursal = request.session['sucursal_id']
    template_name = 'contable/egresos/list.html'
    object_list = Egress.objects.filter(sucursal=sucursal).order_by('-id')
    page_obj = paginacion(request, object_list)
    
    ver_caso_de_gastos()

    context = {
        'title':'Registro de Egresos',
        'page_obj':page_obj,
        'object_list':page_obj,
        'count':object_list.count(),
        'posicion':'Todos los Egresos',
        'permisos':recorrer_los_permisos_usuario(request),
        
    }
        
    return render(request, template_name, context)

class EgresosList(ListView):
    template_name = 'contable/egresos/list.html'
    model = Egress
    paginate_by = 25

    def get_queryset(self):
        try:
            sucursal = self.request.session['sucursal_id']
            query = self.query()
            mes = self.mes_reporte()
            anio = self.anio_reporte()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(fecha__icontains=query)
                filters |= Q(fecha_doc_fiscal__icontains=query)                
                filters |= Q(numero_doc__icontains=query)                
                filters |= Q(codigo_egreso__icontains=query)
                filters |= Q(numero_referencia__icontains=query)
                filters |= Q(nit__icontains=query)
                filters |= Q(nombre__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    
            if mes:
                filters &= Q(fecha__month=mes)

            if anio:
                filters &= Q(fecha__year=anio)

            # Filtrar los objetos Banco usando los filtros definidos
            return Egress.objects.filter(filters, sucursal=sucursal).order_by('-id')
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Egress.objects.none()
    
    def query(self):
        return self.request.GET.get('q')
    
    def mes_reporte(self):
        return self.request.GET.get('mes')
    
    def anio_reporte(self):
        return self.request.GET.get('anio')
    
    @method_decorator(permiso_requerido('puede_ver_registro_egresos'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not context['object_list'] and self.query() is not None:
            messages.error(self.request,'No se encontrado ningun dato')

        # Mantener valores que el usuario eligió en el form
        mes = self.mes_reporte() or datetime.now().month
        anio = self.anio_reporte() or datetime.now().year
        
        consulta = self.query() or ''
        

        context['query'] = consulta
        context['title'] = f'Registro de Egresos'
        context['count'] = context['object_list'].count()
        context['posicion'] = consulta
        context['object_list']  = context['object_list']
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['mes'] = int(mes) if mes else datetime.now().month
        context['anio'] = int(anio) if anio else  datetime.now().year
        return context


@login_required
@usuario_activo
def list_modulos(request):
    template_name = 'contable/options.html'
    
    context = {
        'title':'EL TELAR - MODULOS CONTABLES',
        'acreedores':Creditor.objects.filter(is_paid_off=False),
        'seguros':Insurance.objects.filter(is_paid_off=False),
        'permisos':recorrer_los_permisos_usuario(request),  
    }
        
    return render(request, template_name, context)