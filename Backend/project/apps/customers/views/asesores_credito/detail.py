from django.shortcuts import render, get_object_or_404, redirect

# Models
from apps.customers.models import Customer, CreditCounselor, Cobranza
from apps.financings.models import Credit
from apps.actividades.models import Informe, DetalleInformeCobranza
from apps.users.models import User
from django.db.models import Q

# Decoradores
from django.contrib.auth.decorators import login_required
from project.decorador import permiso_requerido

# MENSAJES
from django.contrib import messages

# SCRIPTS
from scripts.recoleccion_permisos import recorrer_los_permisos_usuario
from scripts.recoleccion_informacion.detalle_asesor_credito import recoleccion_informacion_detalle_asesor

# LIBRERIAS PARA CRUD
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

# Formulario
from apps.customers.forms import CobranzaForms
from datetime import datetime

# utils
from .utils import porcentajes_cobranza

@login_required
@permiso_requerido('puede_visualizar_detalle_asesor_credito')
def detail_asesor(request, codigo_asesor):
    template_name = 'asesores_credito/detail.html'
    asesor_credito = CreditCounselor.objects.filter(codigo_asesor=codigo_asesor).first()

    if asesor_credito is None:
        return redirect('http_404')
    
    context = {
        'title': f'{codigo_asesor}',
        'asesor_credito': asesor_credito,
        'informacion_asesor':recoleccion_informacion_detalle_asesor(asesor_credito),
        'permisos':recorrer_los_permisos_usuario(request)
    }

    return render(request, template_name, context)


class DetailInformeView(TemplateView):
    template_name = 'cobranza/detail.html'
    
    def query(self):
        q = self.request.GET.get('q')
        return q.strip() if q else None


    def get_queryset(self, reporte_id):
        try:
            queryset = DetalleInformeCobranza.objects.filter(reporte_id=reporte_id)

            # Filtro por búsqueda
            if self.query():
                queryset = queryset.filter(
                    Q(cobranza__credito__customer_id__first_name__icontains=self.query()) |
                    Q(cobranza__credito__customer_id__last_name__icontains=self.query()) |
                    Q(cobranza__credito__codigo_credito__icontains=self.query())
                )

            # Filtro por fecha
            fecha = self.request.GET.get("fecha")
            if fecha:
                try:
                    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
                    queryset = queryset.filter(
                        Q(cobranza__fecha_gestion=fecha_dt) |
                        Q(cobranza__fecha_promesa_pago=fecha_dt)
                    )
                except ValueError:
                    pass

            # Filtro por estado de cobranza
            estado = self.request.GET.get("estado_cobranza")
            if estado:
                queryset = queryset.filter(cobranza__estado_cobranza__icontains=estado)

            return queryset

        except Exception as e:
            print(f'Error en get_queryset: {e}')
            return DetalleInformeCobranza.objects.none()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        user_code = kwargs.get("user_code")
        usuario = User.objects.filter(user_code=user_code).first()
        reporte_id = kwargs.get("id")

        # Buscar el reporte
        reporte = get_object_or_404(Informe, id=reporte_id)

        # Obtener los detalles del informe usando get_queryset
        detalles_informe = self.get_queryset(reporte_id)
        
        
        
        if not (detalles_informe):        
            messages.error(self.request,'No se encontrado ningun dato')
        
        posicion = None

        if self.query():
            posicion = self.query()
        elif self.request.GET.get("fecha"):
            posicion = self.request.GET.get("fecha")
        elif self.request.GET.get("estado_cobranza"):
            posicion = self.request.GET.get("estado_cobranza")

     

        

        context.update({
            'title': f'COBRANZA | INFORME | {user_code} | {reporte.fecha_registro} - {reporte.fecha_vencimiento} |',
            'posicion': posicion,
            'permisos': recorrer_los_permisos_usuario(self.request),
            'report': reporte,
            'object_list': detalles_informe,
            'query': self.query() or '',
            'fecha': self.request.GET.get("fecha", ""),
            'estado_cobranza': self.request.GET.get("estado_cobranza", ""),
            'user_code':usuario.user_code,
            'usuario':usuario,
            'form': CobranzaForms(),
            
           
            
        })

        return context

    def get(self, request, *args, **kwargs):
        """
        Sobrescribimos get para asegurar compatibilidad con TemplateView.
        """
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

