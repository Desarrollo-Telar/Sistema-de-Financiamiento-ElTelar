# DECORADORES
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# LIBRERIAS PARA CRUD
from django.views.generic import TemplateView, ListView
from django.db.models import Q

# APPs
from django.apps import apps

# TIEMPO
from datetime import datetime, timedelta

# MODELS
from django.db import models 
from apps.customers.models import Customer, CreditCounselor
from apps.financings.models import Credit

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

# Funcionalidades
from django.db.models import Value, F
from django.db.models.functions import Concat

class Search(TemplateView):
    template_name = 'search.html'
    paginate_by = 25

    def query(self):
        return self.request.GET.get('q', '').strip()

    @method_decorator([usuario_activo])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.query()
        context['query'] = query
        context['title'] = f'Búsqueda: {query}'
        context['posicion'] = query
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        sucursal = self.request.session['sucursal_id']
        request= self.request
        asesor_autenticado = CreditCounselor.objects.filter(usuario=self.request.user).first()

        if query:
            query_lower = query.lower()
            palabras = query_lower.split()

            q_cliente = Q()
            q_credito = Q()

            # Generar filtros por cada palabra
            for palabra in palabras:
                q_cliente |= (
                    Q(first_name__icontains=palabra) |
                    Q(last_name__icontains=palabra) |
                    Q(customer_code__icontains=palabra)
                )

                q_credito |= (
                    Q(codigo_credito__icontains=palabra) |
                    Q(customer_id__customer_code__icontains=palabra) |
                    Q(customer_id__first_name__icontains=palabra) |
                    Q(customer_id__last_name__icontains=palabra)
                )

            # Intentar buscar fechas
            try:
                fecha = datetime.strptime(query, '%Y-%m-%d')
                fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                q_cliente |= Q(creation_date__range=(fecha_inicio, fecha_fin))
                q_credito |= Q(creation_date__range=(fecha_inicio, fecha_fin))
            except ValueError:
                pass

            if asesor_autenticado is not None and request.user.rol.role_name == 'Asesor de Crédito':
                q_credito &= Q(asesor_de_credito=asesor_autenticado)

            roles = ['Programador','Administrador']
            
            if sucursal and not request.user.rol.role_name in roles:
                q_credito &= Q(sucursal=sucursal)

            clientes = Customer.objects.filter(q_cliente).distinct()
            creditos = Credit.objects.filter(q_credito).distinct()

            context['cliente_object'] = clientes
            context['credito_object'] = creditos

        else:
            context['cliente_object'] = Customer.objects.none()
            context['credito_object'] = Credit.objects.none()

        return context