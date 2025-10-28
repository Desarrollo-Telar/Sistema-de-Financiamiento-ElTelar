# Serializador
from apps.financings.api.serializers import CreditSerializer
# MODELS
from apps.financings.models import Credit
from apps.customers.models import Customer, CreditCounselor, Cobranza
from apps.actividades.models import Informe, DetalleInformeCobranza

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request
from rest_framework.exceptions import NotFound

# Tiempo
from datetime import datetime, timedelta

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados


class CreditViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer
    queryset = Credit.objects.all()


    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()
        
        # Filtro por término de búsqueda
        search_term = self.request.query_params.get('term', '')
        # Obtener el mes de creación opcional
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)

        sucursal = getattr(request,'sucursal_actual',None)

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal))

        if search_term:
            queryset = queryset.filter(
                Q(customer_id__first_name__icontains=search_term) |
                Q(customer_id__last_name__icontains=search_term) |
                Q(codigo_credito__icontains=search_term)
            )
        
        

        

        # Filtrar por mes y año si se proporcionan
        if month and year:
            try:
                # Validar que el mes y el año son valores válidos
                month = int(month)
                year = int(year)
                queryset = queryset.filter(
                    created_at__year=year,
                    created_at__month=month
                )
            except ValueError:
                # Si los valores no son válidos, se ignora el filtro de mes/año
                pass

        return queryset
    
    def perform_create(self, serializer):
        credit = serializer.save()
        user = self.request.user
        log_user_action(
            user=user,
            action="Creación de crédito",
            details=f"Se creó el crédito con código {credit.codigo_credito} por un monto de {credit.monto}.",
            request=self.request,
            category_name="Créditos",
            metadata=model_to_dict(credit)
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        previous_data = model_to_dict(instance)
        credit = serializer.save()
        new_data = model_to_dict(credit)

        changes = {
            "antes": previous_data,
            "despues": new_data
        }

        log_user_action(
            user=self.request.user,
            action="Actualización de crédito",
            details=f"Se actualizó el crédito con código {credit.codigo_credito}.",
            request=self.request,
            category_name="Créditos",
            metadata=changes
        )

    
    def perform_destroy(self, instance):
        credit_data = model_to_dict(instance)
        codigo = instance.codigo_credito
        monto = instance.monto

        log_user_action(
            user=self.request.user,
            action="Eliminación de crédito",
            details=f"Se eliminó el crédito con código {codigo} por un monto de {monto}.",
            request=self.request,
            category_name="Créditos",
            metadata=credit_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de crédito",
                details=f"Se eliminó el crédito con código {codigo} por un monto de {monto}.",
                request=self.request,
                category_name="Créditos",
                metadata=credit_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el crédito con código {codigo}: {str(e)}",
                level_name="ERROR",
                source="CreditViewSet.perform_destroy",
                category_name="Créditos",
                traceback=traceback.format_exc(),
                metadata=credit_data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500



class CreditVigentesViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer

    def get_queryset(self):
        queryset = Credit.objects.filter(Q(is_paid_off=False) | Q(estado_judicial=False))
        search_term = self.request.query_params.get('term', '').strip()

        # Obtener el asesor autenticado
        asesor_autenticado = CreditCounselor.objects.filter(usuario=self.request.user).first()
        roles = ['Administrador', 'Programador']

        sucursal = getattr(self.request,'sucursal_actual',None)

        if sucursal:
            queryset = queryset.filter(Q(sucursal=sucursal))

        if search_term:
            filters = (
                Q(customer_id__first_name__icontains=search_term) |
                Q(customer_id__last_name__icontains=search_term) |
                Q(codigo_credito__icontains=search_term)
            )

            if asesor_autenticado:
                if not self.request.user.rol.role_name in roles:
                    filters &= Q(asesor_de_credito__id=asesor_autenticado.id)

            queryset = queryset.filter(filters)

        elif asesor_autenticado:
            # Si no hay término de búsqueda, pero sí asesor autenticado, filtrar por él
            if not self.request.user.rol.role_name in roles:
                queryset = queryset.filter(asesor_de_credito__id=asesor_autenticado.id)

        return queryset
    
    def perform_create(self, serializer):
        credit = serializer.save()
        user = self.request.user
        log_user_action(
            user=user,
            action="Creación de crédito",
            details=f"Se creó el crédito con código {credit.codigo_credito} por un monto de {credit.monto}.",
            request=self.request,
            category_name="Créditos",
            metadata=model_to_dict(credit)
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        previous_data = model_to_dict(instance)
        credit = serializer.save()
        new_data = model_to_dict(credit)

        changes = {
            "before": previous_data,
            "after": new_data
        }

        log_user_action(
            user=self.request.user,
            action="Actualización de crédito",
            details=f"Se actualizó el crédito con código {credit.codigo_credito}.",
            request=self.request,
            category_name="Créditos",
            metadata=changes
        )

    
    def perform_destroy(self, instance):
        credit_data = model_to_dict(instance)
        codigo = instance.codigo_credito
        monto = instance.monto

        log_user_action(
            user=self.request.user,
            action="Eliminación de crédito",
            details=f"Se eliminó el crédito con código {codigo} por un monto de {monto}.",
            request=self.request,
            category_name="Créditos",
            metadata=credit_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de crédito",
                details=f"Se eliminó el crédito con código {codigo} por un monto de {monto}.",
                request=self.request,
                category_name="Créditos",
                metadata=credit_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el crédito con código {codigo}: {str(e)}",
                level_name="ERROR",
                source="CreditViewSet.perform_destroy",
                category_name="Créditos",
                traceback=traceback.format_exc(),
                metadata=credit_data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500


from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.db.models import Q

class CreditVigentesCobranzaViewSet(viewsets.ModelViewSet):
    serializer_class = CreditSerializer

    def get_queryset(self):
        base_qs = Credit.objects.filter(is_paid_off=False, estado_judicial=False)
        search_term = self.request.query_params.get('term', '').strip()

        asesor_autenticado = CreditCounselor.objects.filter(usuario=self.request.user).first()
        reporte_id = Informe.objects.filter(usuario=self.request.user, esta_activo=True).first()
        roles = ['Administrador', 'Programador']
        role_name = getattr(getattr(self.request.user, 'rol', None), 'role_name', None)

        sucursal = getattr(self.request, 'sucursal_actual', None)

        # Validar usuario e informe activo
        if not asesor_autenticado or not reporte_id:
            raise NotFound("No se encontró información para este usuario.")

        # Si hay sucursal, filtra el queryset base
        if sucursal:
            base_qs = base_qs.filter(sucursal=sucursal)

        # Excluir los créditos que ya están en el informe vigente
        informe_vigente = DetalleInformeCobranza.objects.filter(reporte_id=reporte_id)
        creditos_con_cobranza = Credit.objects.filter(
            id__in=informe_vigente.values_list("cobranza__credito_id", flat=True)
        )

        queryset = base_qs.filter(estados_fechas=False).exclude(id__in=creditos_con_cobranza)

        # Aplicar filtros de búsqueda
        if search_term:
            filters = (
                Q(customer_id__first_name__icontains=search_term) |
                Q(customer_id__last_name__icontains=search_term) |
                Q(codigo_credito__icontains=search_term)
            )
            if role_name not in roles:
                filters &= Q(asesor_de_credito__id=asesor_autenticado.id)
            queryset = queryset.filter(filters)
        elif role_name not in roles:
            queryset = queryset.filter(asesor_de_credito__id=asesor_autenticado.id)

        return queryset

    def perform_create(self, serializer):
        credit = serializer.save()
        user = self.request.user
        log_user_action(
            user=user,
            action="Creación de crédito",
            details=f"Se creó el crédito con código {credit.codigo_credito} por un monto de {credit.monto}.",
            request=self.request,
            category_name="Créditos",
            metadata=model_to_dict(credit)
        )
    
    def perform_update(self, serializer):
        instance = self.get_object()
        previous_data = model_to_dict(instance)
        credit = serializer.save()
        new_data = model_to_dict(credit)

        changes = {
            "before": previous_data,
            "after": new_data
        }

        log_user_action(
            user=self.request.user,
            action="Actualización de crédito",
            details=f"Se actualizó el crédito con código {credit.codigo_credito}.",
            request=self.request,
            category_name="Créditos",
            metadata=changes
        )

    
    def perform_destroy(self, instance):
        credit_data = model_to_dict(instance)
        codigo = instance.codigo_credito
        monto = instance.monto

        log_user_action(
            user=self.request.user,
            action="Eliminación de crédito",
            details=f"Se eliminó el crédito con código {codigo} por un monto de {monto}.",
            request=self.request,
            category_name="Créditos",
            metadata=credit_data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de crédito",
                details=f"Se eliminó el crédito con código {codigo} por un monto de {monto}.",
                request=self.request,
                category_name="Créditos",
                metadata=credit_data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el crédito con código {codigo}: {str(e)}",
                level_name="ERROR",
                source="CreditViewSet.perform_destroy",
                category_name="Créditos",
                traceback=traceback.format_exc(),
                metadata=credit_data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500
