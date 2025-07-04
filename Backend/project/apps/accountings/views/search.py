
# Manejo de mensajes
from django.contrib import messages

# Models
from apps.accountings.models import Creditor, Insurance,  Income


# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from project.decorador import  permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# MENSAJES
from django.contrib import messages

class AcreedoresSearch(ListView):
    template_name = 'contable/acreedores/list.html'
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
                filters |= Q(nombre_acreedor__icontains=query)                
                filters |= Q(codigo_acreedor__icontains=query)
                filters |= Q(numero_referencia__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    filters |= Q(plazo__exact=query)
                    filters |= Q(tasa__exact=query)
                    

            # Filtrar los objetos Banco usando los filtros definidos
            return Creditor.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Creditor.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(permiso_requerido('puede_consultar_acreedores'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = f'Registro de Acreedores con {self.query()}'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query()
        context['acreedores_list']  = context['object_list']
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context

class SeguroSearch(ListView):
    template_name = 'contable/seguros/list.html'
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
                filters |= Q(nombre_acreedor__icontains=query)                
                filters |= Q(codigo_seguro__icontains=query)
                filters |= Q(numero_referencia__icontains=query)
                

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    filters |= Q(plazo__exact=query)
                    filters |= Q(tasa__exact=query)
                    

            # Filtrar los objetos Banco usando los filtros definidos
            return Insurance.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Insurance.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(permiso_requerido('puede_consultar_seguros'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = f'Registro de Seguros con {self.query()}.'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query()
        context['object_list']  = context['object_list']
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context

class IngresoSearch(ListView):
    template_name = 'contable/ingresos/list.html'
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
                filters |= Q(codigo_ingreso__icontains=query)                
                           
                
                filters |= Q(numero_referencia__icontains=query)

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    
                    
                    

            # Filtrar los objetos Banco usando los filtros definidos
            return Income.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Income.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(permiso_requerido('puede_consultar_ingresos'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = f'Registro de Ingresos con {self.query()}'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query()
        context['object_list']  = context['object_list']
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context

class EgresoSearch(ListView):
    template_name = 'contable/egresos/list.html'
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
                filters |= Q(fecha_doc_fiscal__icontains=query)                
                filters |= Q(numero_doc__icontains=query)                
                filters |= Q(codigo_seguro__icontains=query)
                filters |= Q(numero_referencia__icontains=query)
                

                # Si la consulta es numérica, usar filtro exacto para campos numéricos
                if query.isdigit():
                    filters |= Q(monto__exact=query)
                    filters |= Q(plazo__exact=query)
                    filters |= Q(tasa__exact=query)
                    

            # Filtrar los objetos Banco usando los filtros definidos
            return Insurance.objects.filter(filters)
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Insurance.objects.none()
    

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(permiso_requerido('puede_consultar_egresos'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')
        context['query'] = self.query()
        context['title'] = f'Registro de Egresos con {self.query()}'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query()
        context['object_list']  = context['object_list']
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context