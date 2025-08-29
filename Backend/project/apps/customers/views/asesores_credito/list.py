# URLS
from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Cobranza, CreditCounselor, HistorialCobranza
from apps.actividades.models import Informe

# LIBRERIAS PARA CRUD
from django.views.generic import ListView, TemplateView
from django.db.models import Q

# Formulario
from apps.customers.forms import CobranzaForms

# Decoradores
from project.decorador import permiso_requerido
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# MENSAJES
from django.contrib import messages

# TIEMPO
from datetime import datetime, timedelta, timezone

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario


@login_required
def view_historial_cobranza(request, id):
    template_name = 'cobranza/historial.html'
    historial_cobranza = HistorialCobranza.objects.filter(cobranza__id = id)
    context = {
        'object_list':historial_cobranza
    }

    return render(request, template_name, context )

@login_required
@permiso_requerido('puede_ver_registros_cobranza')
def view_gestion(request):
    # Verificar si existe un informe vigente para el usuario
    informe_vigente = Informe.objects.filter(
        usuario=request.user,
        esta_activo=True
    ).order_by('-id').first()

    if not informe_vigente:
        # Si no existe, crear uno nuevo
        informe_vigente = Informe.objects.create(
            usuario=request.user,
            esta_activo=True
        )
    return redirect('customers:detail_informe_cobranza',request.user.user_code, informe_vigente.id) 

class CobranzaList(TemplateView):
    template_name = 'cobranza/list.html'

    def get_queryset(self):
        try:
            # Verificar si existe un informe vigente para el usuario
            informe_vigente = Informe.objects.filter(
                usuario=self.request.user,
                esta_activo=True
            ).order_by('-id').first()

            if not informe_vigente:
                # Si no existe, crear uno nuevo
                informe_vigente = Informe.objects.create(
                    usuario=self.request.user,
                    esta_activo=True,
                    fecha_registro=timezone.now()
                )

            queryset = Informe.objects.filter(usuario=self.request.user).order_by('-id')

            # Si hay búsqueda
            query = self.query()
            if query:
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                    queryset = queryset.filter(fecha_registro__range=(fecha_inicio, fecha_fin))
                except ValueError:
                    pass  # No es fecha válida

            return queryset

        except Exception as e:
            print(f'error: {e}')
            return Informe.objects.none()

    @method_decorator([permiso_requerido('puede_ver_registros_cobranza')])
    def dispatch(self, request, *args, **kwargs):
        asesor_credito = CreditCounselor.objects.filter(usuario=request.user).first()
        if not asesor_credito:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

       

        if self.query():
            context['query'] = self.query()

        consulta = self.query() or ''

        context['title'] = f'Asesores de Creditos | Cobranza |{consulta}'
        
        context['posicion'] = f"{self.request.user.first_name} {self.request.user.last_name}"
        context['permisos'] = recorrer_los_permisos_usuario(self.request)
        context['form'] = CobranzaForms()
        context['usuario'] = self.request.user
        context['user_code'] = self.request.user.user_code
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
                try:
                    fecha = datetime.strptime(query, '%Y-%m-%d')
                    fecha_inicio = datetime.combine(fecha.date(), datetime.min.time())
                    fecha_fin = datetime.combine(fecha.date(), datetime.max.time())
                    filters |= Q()
                except ValueError:
                    pass  # No es fecha válida, continúa con los otros filtros
                filters |= Q(nombre__icontains = query)
                filters |= Q(apellido__icontains = query)             
                filters |= Q(codigo_asesor__icontains = query)


            return CreditCounselor.objects.filter(filters).order_by('id')
        
        except Exception as e:
            print(f'error: {e}')
            
            return CreditCounselor.objects.all().order_by('id')
    
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
        context['usuario'] = self.request.user
        return context