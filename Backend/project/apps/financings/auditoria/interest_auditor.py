
from datetime import datetime
from decimal import Decimal

from django.utils import timezone

from .engine import dinero
from .repository import CreditAuditRepository


class InterestAuditor:
    """
    Auditor de intereses mensuales.

    Reconstruye el interés de cada período utilizando
    capital original, tasa mensual y pagos de capital.

    No modifica información de la base de datos.
    """

    def __init__(self):
        self.repo = CreditAuditRepository()

    @staticmethod
    def fecha(valor):
        if isinstance(valor, datetime):
            if timezone.is_aware(valor):
                return timezone.localtime(valor).date()
            return valor.date()
        return valor

    def analizar(self, credito_id):
        credito = self.repo.obtener_credito(credito_id)
        pagos = self.repo.obtener_pagos(credito)
        cuotas = self.repo.obtener_cuotas(credito)

        capital = dinero(credito.monto)
        tasa = Decimal(str(credito.tasa_interes))

        # La tasa se interpreta como decimal:
        # 0.10 = 10% mensual.
        if tasa < 0 or tasa > 1:
            raise ValueError(
                "Verifica el formato de tasa_interes. "
                "Este auditor espera 0.10 para representar 10%."
            )

        pagos_ordenados = sorted(
            pagos,
            key=lambda p: (
                self.fecha(p["fecha_emision"]),
                p["fecha_emision"],
                p["id"],
            ),
        )

        cuotas_ordenadas = sorted(
            cuotas,
            key=lambda c: (
                self.fecha(c["due_date"]),
                c["id"],
            ),
        )

        resultados = []
        diferencias = []
        indice_pago = 0

        for cuota in cuotas_ordenadas:
            vencimiento = self.fecha(cuota["due_date"])

            if vencimiento is None:
                diferencias.append({
                    "cuota_id": cuota["id"],
                    "tipo": "VENCIMIENTO_AUSENTE",
                })
                continue

            # Aplicamos los abonos a capital realizados
            # antes del vencimiento de esta cuota.
            #
            # Un pago realizado el mismo día se considera
            # posterior a la generación del interés.
            while indice_pago < len(pagos_ordenados):
                pago = pagos_ordenados[indice_pago]
                fecha_pago = self.fecha(pago["fecha_emision"])

                if fecha_pago >= vencimiento:
                    break

                capital_pagado = dinero(
                    pago["capital"] or 0
                )

                capital = dinero(
                    capital - capital_pagado
                )

                indice_pago += 1

            interes_calculado = dinero(capital * tasa)

            # Esta columna representa el interés
            # generado que conserva el sistema.
            interes_registrado = dinero(
                cuota["interes_generado"] or 0
            )

            diferencia = dinero(
                interes_calculado - interes_registrado
            )

            resultado = {
                "cuota_id": cuota["id"],
                "mes": cuota["mes"],
                "vencimiento": vencimiento,
                "capital_base": capital,
                "tasa": tasa,
                "interes_calculado": interes_calculado,
                "interes_registrado": interes_registrado,
                "diferencia": diferencia,
            }

            resultados.append(resultado)

            if diferencia != Decimal("0.00"):
                diferencias.append({
                    **resultado,
                    "tipo": "DIFERENCIA_INTERES_GENERADO",
                })

        return {
            "credito_id": credito.pk,
            "codigo": str(credito),
            "capital_inicial": dinero(credito.monto),
            "tasa_mensual": tasa,
            "cuotas_analizadas": len(resultados),
            "total_diferencias": len(diferencias),
            "resultados": resultados,
            "diferencias": diferencias,
        }
