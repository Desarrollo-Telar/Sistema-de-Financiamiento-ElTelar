from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Models
from apps.customers.models import Customer, CreditCounselor, Cobranza
from apps.financings.models import Credit
from apps.actividades.models import Informe, DetalleInformeCobranza
from django.db.models import Q

# Seralzer
from apps.financings.api.serializers import CreditSerializer

class InformacionAsesorCobranzaView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios logueados

    def get(self, request, user_code):
        # Buscar asesor y reporte vigente
        asesor_credito = CreditCounselor.objects.filter(usuario__user_code=user_code).first()
        reporte_id = Informe.objects.filter(usuario__user_code=user_code, esta_activo=True).first()

        if not asesor_credito or not reporte_id:
            return Response({
                "detail": "No se encontró información para este usuario."
            }, status=404)

        # Créditos del asesor que no están pagados ni judiciales
        creditos_asesor = Credit.objects.filter(
            asesor_de_credito__id=asesor_credito.id,
            is_paid_off=False,
            estado_judicial=False
        )

        # Todas las cobranzas registradas en el informe
        informe_vigente = DetalleInformeCobranza.objects.filter(reporte_id=reporte_id)

        # Créditos ya con cobranza
        creditos_con_cobranza = Credit.objects.filter(
            id__in=informe_vigente.values_list("cobranza__credito_id", flat=True)
        )

        # Créditos faltantes = todos los del asesor - los con cobranza
        creditos_faltantes = creditos_asesor.filter(estados_fechas=False).exclude(id__in=creditos_con_cobranza.values_list("id", flat=True))


        return Response({
            "total_creditos": creditos_asesor.count(),
            "total_realizados": creditos_con_cobranza.count(),
            "total_faltantes": creditos_faltantes.count(),
            "creditos_realizados": CreditSerializer(creditos_con_cobranza, many=True).data,
            "creditos_faltantes": CreditSerializer(creditos_faltantes, many=True).data,
            "creditos_vigentes":creditos_asesor.data,
        })
