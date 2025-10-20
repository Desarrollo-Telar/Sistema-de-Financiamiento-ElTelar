# TIEMPO
from datetime import datetime, timedelta

# Models
from apps.financings.models import Invoice

# Manejo de mensajes
from django.contrib import messages

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# Scripts
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

#puede_ver_facturas

class ListadoFacturas(ListView):
    template_name = 'financings/factura/listado.html'
    paginate_by = 50

    def get_queryset(self):
        try:
            sucursal = self.request.session['sucursal_id']
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()

            # Añadir filtros si la consulta no está vacía
            if query:
                filters |= Q(issue_date__icontains=query)
                filters |= Q(recibo_id__pago__numero_referencia__icontains=query)
                filters |= Q(nit_receptor__icontains=query)
                filters |= Q(nombre_receptor__icontains=query)
                filters |= Q(numero_autorizacion__icontains=query)
                filters |= Q(serie_autorizacion__icontains=query)

            # Filtrar los objetos Banco usando los filtros definidos
            return Invoice.objects.filter(filters, sucursal=sucursal).order_by('-id')
        
        except Exception as e:
            # Manejar cualquier excepción que ocurra y devolver un queryset vacío
            print(f"Error al filtrar el queryset: {e}")
            return Invoice.objects.none()

    def query(self):
        return self.request.GET.get('q')
    
    @method_decorator(permiso_requerido('puede_ver_facturas'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context