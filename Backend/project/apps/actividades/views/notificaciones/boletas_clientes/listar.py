# Models
from apps.actividades.models import DocumentoNotificacionCliente

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q



# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator

# MENSAJES
from django.contrib import messages

# TIEMPO
from datetime import datetime, timedelta

# URLS
from django.shortcuts import redirect

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# 

class DocumentoNotificacionClientesList(ListView):
    model = DocumentoNotificacionCliente
    template_name = 'customer/boletas_clientes/list.html'
    paginate_by = 50

    def get_queryset(self):
        sucursal = self.request.session['sucursal_id']
        try:
            query = self.query()
            filters = Q()

            if query:
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                    filters |= Q(created_at__range=(fecha_inicio, fecha_fin))
                except ValueError:
                    pass

                filters |= Q(status__icontains=query)
                filters |= Q(cliente__first_name__icontains=query)
                filters |= Q(cliente__last_name__icontains=query)
                filters |= Q(cliente__customer_code__icontains=query)
                filters |= Q(cuota__credit_id__codigo_credito__icontains=query)

            return DocumentoNotificacionCliente.objects.filter(filters, sucursal=sucursal).order_by('-fecha_actualizacion')

        except Exception as e:
            print(f'error: {e}')
            return DocumentoNotificacionCliente.objects.filter(sucursal=sucursal).order_by('-fecha_actualizacion')

    def query(self):
        return self.request.GET.get('q')

    @method_decorator([permiso_requerido('puede_ver_registro_boletas')])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Agregamos el rango elidido a page_obj para la plantilla de paginación
        if context.get('is_paginated'):
            page_obj = context['page_obj']
            page_obj.custom_page_range = page_obj.paginator.get_elided_page_range(
                page_obj.number, on_each_side=2, on_ends=1
            )

        if not context['object_list']:
            messages.error(self.request, 'No se ha encontrado ningún dato')

        if self.query():
            context['query'] = self.query()

        consulta = self.query() or ''

        context['title'] = f'Boletas Subidas Por Clientes | {consulta}'
        
        # 2. Conteo del total general de registros (no solo los 50 de la página actual)
        if context.get('paginator'):
            context['count'] = context['paginator'].count
        else:
            context['count'] = len(context['object_list'])

        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['usuario'] = self.request.user
        return context