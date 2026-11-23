import os
import django
from django.utils import timezone

# Configura Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # <-- Ajusta si tu settings está en otro path
django.setup()

from apps.financings.models import AccountStatement

if __name__ == "__main__":
    print("Pruebas")
    print("Revisión de los últimos estados de cuenta...")

    dia = timezone.localdate()

    ultimos_estados = (
        AccountStatement.objects.filter(
            description="PAGO DE CREDITO",
            credit__isnull=False,
        )
        .select_related("credit", "payment", "cuota")
        .order_by("credit_id", "-creation_date", "-id")
        .distinct("credit_id")
    )

    print(ultimos_estados.count())

    for estado in ultimos_estados:
        credito = estado.credit

        if (
            credito is not None
            and not credito.is_paid_off
            and not credito.estado_judicial
            and credito.categoria_credito_demandado is None
            and estado.issue_date is not None
        ):
            fecha_diferencia = (dia - estado.issue_date).days
           

            if fecha_diferencia > 15 and credito.estados_fechas == True:

                print(f" {credito.id} {credito.estados_fechas}")