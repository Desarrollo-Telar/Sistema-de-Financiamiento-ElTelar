# lOGS
import logging
logger = logging.getLogger(__name__)

# MODELOS
from apps.financings.models import  Credit
from apps.accountings.models import Creditor, Insurance

from django.db.models import Q

from apps.codes.models import TokenCliente


def get_credito(cuota):
    logger.info("OBTENIENDO EL CREDITO")
    credito = None

    if cuota.credit_id is not None:
        credito =  Credit.objects.get(id=cuota.credit_id.id)

        if credito.estado_judicial:
            return None
    
    if cuota.acreedor is not None:
        credito =  Creditor.objects.get(id=cuota.acreedor.id)
    
    if cuota.seguro is not None:
        credito =  Insurance.objects.get(id=cuota.seguro.id)

    return credito