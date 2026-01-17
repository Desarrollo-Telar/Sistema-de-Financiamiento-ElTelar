
# Serializador
from apps.financings.api.serializers import  ReciboSerializer

# MODELS
from apps.financings.models import  Recibo

# API
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import datetime

from rest_framework.request import Request

# Tiempo
from datetime import datetime, timedelta

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

import traceback
from rest_framework import status
from rest_framework.exceptions import ValidationError

class ReciboViewSet(viewsets.ModelViewSet):
    serializer_class = ReciboSerializer
    queryset = Recibo.objects.all()

    def get_queryset(self):
        # Obtener parámetros de la solicitud
        request = self.request
        query_params = request.query_params

        # Valores predeterminados
        mes = query_params.get('mes', datetime.now().month)
        anio = query_params.get('anio', datetime.now().year)
        filtro_seleccionado = query_params.get('filtro', 'mora_pagada')

        try:
            mes = int(mes)
            anio = int(anio)
        except ValueError:
            mes = datetime.now().month
            anio = datetime.now().year

        # Filtros por fecha
        filters = Q(fecha__year=anio, fecha__month=mes)

        # Filtros dinámicos según selección del usuario
        filtros_validos = {
            'mora_pagada': 'mora_pagada__gt',
            'interes_pagado': 'interes_pagado__gt',
            'aporte_capital': 'aporte_capital__gt',
        }

        if filtro_seleccionado in filtros_validos:
            filtro_dinamico = {filtros_validos[filtro_seleccionado]: 0}
            return Recibo.objects.filter(filters, **filtro_dinamico)

        return Recibo.objects.filter(filters)

    def perform_create(self, serializer):
        try:
            
            data = serializer.save()
            user = self.request.user

            # 2. Intentamos registrar la acción exitosa
            log_user_action(
                user=user,
                action="Creación de Recibo",
                details=f"Se creó un Recibo {data.id} .",
                request=self.request,
                category_name="Recibos",
                metadata=model_to_dict(data)
            )

        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al crear el recibo o registrar log: {str(e)}",
                level_name="ERROR",
                source="ReciboViewSet.perform_create",
                category_name="Recibos",
                traceback=error_stack,
                metadata={
                    "request_data": self.request.data,
                    "user_attempting": str(self.request.user)
                }
            )
            
            # 4. Relanzamos una excepción para que el cliente reciba un error 400/500
            raise ValidationError({
                "error": "No se pudo completar la operación. El incidente ha sido reportado al sistema."
            })
    
    def perform_update(self, serializer):
        try:
            instance = self.get_object()
            previous_data = model_to_dict(instance)
            data = serializer.save()
            new_data = model_to_dict(data)

            changes = {
                "antes": previous_data,
                "despues": new_data
            }

            log_user_action(
                user=self.request.user,
                action="Actualización de Recibo",
                details=f"Se actualizó el recibo. {data.id}.",
                request=self.request,
                category_name="Recibos",
                metadata=changes
            )
        except Exception as e:
            # 3. Si algo falla, capturamos el error y el traceback
            error_stack = traceback.format_exc()
            
            log_system_event(
                message=f"Error al actualizar el recibo o registrar log: {str(e)}",
                level_name="ERROR",
                source="ReciboViewSet.perform_update",
                category_name="Recibos",
                traceback=error_stack,
                metadata={
                    "request_data": self.request.data,
                    "user_attempting": str(self.request.user)
                }
            )
            
            # 4. Relanzamos una excepción para que el cliente reciba un error 400/500
            raise ValidationError({
                "error": "No se pudo completar la operación. El incidente ha sido reportado al sistema."
            })

    def perform_destroy(self, instance):
        data = model_to_dict(instance)
        nombre = f'{instance.id}'
        

        log_user_action(
            user=self.request.user,
            action="Eliminación de recibo",
            details=f"Se eliminó el recibo: {nombre}.",
            request=self.request,
            category_name="Recibos",
            metadata=data
        )

        try:
            instance.delete()
            log_user_action(
                user=self.request.user,
                action="Eliminación de recibo",
                details=f"Se eliminó el recibo: {nombre}.",
                request=self.request,
                category_name="Recibos",
                metadata=data
            )

        except Exception as e:
            import traceback
            log_system_event(
                message=f"Error al eliminar el recibo. {nombre}: {str(e)}",
                level_name="ERROR",
                source="ReciboViewSet.perform_destroy",
                category_name="Recibos",
                traceback=traceback.format_exc(),
                metadata=data
            )
            raise  # re-lanza el error para que DRF devuelva la respuesta HTTP 500


