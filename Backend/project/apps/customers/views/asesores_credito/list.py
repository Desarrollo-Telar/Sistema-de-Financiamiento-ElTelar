
# Models
from apps.customers.models import Cobranza, CreditCounselor
from apps.actividades.models import Informe

# LIBRERIAS PARA CRUD
from django.views.generic.list import ListView
from django.db.models import Q

# Formulario
from apps.customers.forms import CobranzaForms

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

class CobranzaList(ListView):
    model = Informe
    template_name = 'cobranza/list.html'
    paginate_by = 12

    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()
            filters &= Q(usuario=self.request.user)

            if query:
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                    filters |= Q(fecha_registro__range=(fecha_inicio, fecha_fin))
                except ValueError:
                    pass  # No es fecha válida, continúa con los otros filtros


            return Informe.objects.filter(filters).order_by('-id')
        
        except Exception as e:
            print(f'error: {e}')
            
            return Informe.objects.none()
    
    @method_decorator([permiso_requerido('puede_ver_registros_cobranza')])
    def dispatch(self, request, *args, **kwargs):
        asesor_credito = CreditCounselor.objects.filter(usuario=request.user).first()
        if not asesor_credito:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('index')  # Usa el nombre de la URL de tu index
        return super().dispatch(request, *args, **kwargs)
    
    def query(self):
        return self.request.GET.get('q')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not (context['object_list']):
            if self.query():
                messages.error(self.request,'No se encontrado ningun dato')

        if self.query():
            context['query'] = self.query()
            
            
        consulta = self.query()
        if consulta is None:
            consulta = ''

        
        context['title'] = f'Asesores de Creditos | Cobranza |{consulta}'
        context['count'] = context['object_list'].count()
        context['posicion'] =  f"{self.request.user.first_name} {self.request.user.last_name}"
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['form'] = CobranzaForms()
        return context
    

class AsesoresCreditosList(ListView):
    model = CreditCounselor
    template_name = 'asesores_credito/list.html'
    paginate_by = 50

    
    
    def get_queryset(self):
        try:
            # Asignar la consulta a una variable local
            query = self.query()

            # Crear una lista para almacenar los filtros
            filters = Q()
            

            if query:
                filters |= Q(nombre__icontains = query)
                filters |= Q(apellido__icontains = query)             
                filters |= Q(codigo_asesor__icontains = query)


            return CreditCounselor.objects.filter(filters).order_by('id')
        
        except Exception as e:
            print(f'error: {e}')
            
            return CreditCounselor.objects.none()
    
    @method_decorator([permiso_requerido('puede_ver_registros_asesores')])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def query(self):
        return self.request.GET.get('q')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not (context['object_list']):
            messages.error(self.request,'No se encontrado ningun dato')

        if self.query():
            context['query'] = self.query()
            
            
        consulta = self.query()
        if consulta is None:
            consulta = ''

        
        context['title'] = f'Asesores de Creditos | {consulta}'
        context['count'] = context['object_list'].count()
        context['posicion'] = self.query() if self.query() else ''
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        return context