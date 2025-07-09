# DECORADORES
from project.decorador import usuario_activo
from django.utils.decorators import method_decorator

# LIBRERIAS PARA CRUD
from django.views.generic import TemplateView, ListView
from django.db.models import Q

# APPs
from django.apps import apps

# MODELS
from django.db import models 
from apps.customers.models import Customer
from apps.financings.models import Credit

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario

class Search(TemplateView):
    template_name = 'search.html'
    paginate_by = 25

    def query(self):
        return self.request.GET.get('q')

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

        if query:
            try:
                customer_filters = (
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(customer_code__icontains=query)
                )

                credit_filters = (
                    Q(codigo_credito__icontains=query) |
                    Q(customer_id__customer_code__icontains=query)|
                    Q(customer_id__first_name__icontains=query)|
                    Q(customer_id__last_name__icontains=query)
                )

                clientes = Customer.objects.filter(customer_filters)
                creditos = Credit.objects.filter(credit_filters)

                context['cliente_object'] = clientes
                context['credito_object'] = creditos

            except Exception as e:
                print(f"Error en búsqueda: {e}")
                context['cliente_object'] = Customer.objects.none()
                context['credito_object'] = Credit.objects.none()
        else:
            context['cliente_object'] = Customer.objects.none()
            context['credito_object'] = Credit.objects.none()

        return context



