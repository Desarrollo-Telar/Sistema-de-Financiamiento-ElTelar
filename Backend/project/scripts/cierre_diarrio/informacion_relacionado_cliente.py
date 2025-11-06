
from apps.customers.models import Customer
from apps.customers.api.serializers import CustomerSerializer

from apps.addresses.models import Address
from apps.FinancialInformation.models import Reference, OtherSourcesOfIncome, WorkingInformation
from apps.InvestmentPlan.models import InvestmentPlan
from apps.financings.models import Credit

# HISTORIAL Y BITACORA
from apps.actividades.utils import log_user_action, log_system_event
from scripts.conversion_datos import model_to_dict, cambios_realizados

# Tiempo
from datetime import datetime,timedelta

from rest_framework.renderers import JSONRenderer  # Para forzar conversión JSON pura
import json



def generando_informacion_cliente(sucursal):
    # ⚙️ No usar iterator() con DRF, usar queryset normal o list()
    informacion_cliente = Customer.objects.filter(sucursal=sucursal)

    # 🔹 Serializa a dict seguro (sin referencias a objetos)
    serializer = CustomerSerializer(informacion_cliente, many=True)
    clientes_serializados = serializer.data  # Ya son OrderedDicts JSON-safe

            # 🔹 Asegurar que todo sea JSON serializable
    clientes_json = JSONRenderer().render(clientes_serializados)
    clientes_data = json.loads(clientes_json)  # Convierte a lista/dict puro
    return clientes_data


