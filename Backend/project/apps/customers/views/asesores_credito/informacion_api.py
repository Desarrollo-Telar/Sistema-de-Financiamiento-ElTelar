from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Models
from apps.customers.models import Customer, CreditCounselor, Cobranza
from apps.users.models import User
from apps.financings.models import Credit
from apps.actividades.models import Informe, DetalleInformeCobranza
from apps.subsidiaries.models import Subsidiary
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat
# Seralzer
from apps.financings.api.serializers import CreditSerializer

class InformacionAsesorCobranzaView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios logueados

    def get(self, request, user_code):
        # Buscar asesor y reporte vigente
        asesor_credito = CreditCounselor.objects.filter(usuario__user_code=user_code).first()
        reporte_id = Informe.objects.filter(usuario__user_code=user_code, esta_activo=True).first()

        roles = ['Administrador', 'Programador','Secretari@']
        role_name = getattr(getattr(request.user, 'rol', None), 'role_name', None)
        #usuario = User.objects.get(user_code=user_code)
        #role_name = usuario.rol

        sucursal = request.session['sucursal_id']
        

        filtros = Q()

        if not asesor_credito or not reporte_id:
            return Response({
                "detail": "No se encontró información para este usuario."
            }, status=404)
        
        filtros &= Q(is_paid_off=False)
        filtros &= Q(estado_judicial=False)

        if sucursal:
            filtros &= Q(sucursal__id=sucursal)

        if role_name in roles:
            asesores = CreditCounselor.objects.filter(id__in=[7, 4])

            if sucursal != 2:
                filtros &= Q(asesor_de_credito__in = asesores) 
            else:
                filtros &= Q(asesor_de_credito__id = 7)

        else:
            filtros &= Q(asesor_de_credito__id=asesor_credito.id)

        # Créditos del asesor que no están pagados ni judiciales
        creditos_asesor = Credit.objects.filter(filtros, sucursal=sucursal)

        # Todas las cobranzas registradas en el informe
        informe_vigente = DetalleInformeCobranza.objects.filter(reporte_id=reporte_id)

        # Créditos ya con cobranza
        creditos_con_cobranza = Credit.objects.filter(
            id__in=informe_vigente.values_list("cobranza__credito_id", flat=True)
        )

        # Créditos faltantes = todos los del asesor - los con cobranza
        creditos_faltantes = creditos_asesor.filter(estados_fechas=False, sucursal=sucursal).exclude(id__in=creditos_con_cobranza.values_list("id", flat=True))


        return Response({
            "total_creditos": creditos_asesor.count(),
            "total_realizados": creditos_con_cobranza.count(),
            "total_faltantes": creditos_faltantes.count(),
            "creditos_realizados": CreditSerializer(creditos_con_cobranza, many=True).data,
            "creditos_faltantes": CreditSerializer(creditos_faltantes, many=True).data,
            "creditos_vigentes": CreditSerializer(creditos_asesor,many=True).data,
        })
