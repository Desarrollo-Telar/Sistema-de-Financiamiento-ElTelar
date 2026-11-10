
from decimal import Decimal
from .engine import dinero
from .repository import CreditAuditRepository


class CreditLedgerAuditor:
    """
    Libro mayor de auditoría, exclusivamente de lectura.

    Fase 1:
    - Reconstruye capital desde el monto original.
    - Verifica distribución contable de cada pago.
    - Detecta capital negativo.
    - No presume que la distribución histórica sea correcta.
    """

    def __init__(self, credito_id):
        self.credito_id = credito_id

    def ejecutar(self):
        credito = CreditAuditRepository.obtener_credito(
            self.credito_id
        )

        tipo_proceso = (credito.tipo_proceso or "").strip().upper()

        if tipo_proceso != "NORMAL":
            return {
                "credito_id": self.credito_id,
                "estado": "REVISION_MANUAL",
                "motivo": (
                    "El crédito utiliza un proceso de pago extraordinario "
                    f"({tipo_proceso or 'NO DEFINIDO'})."
                ),
                "movimientos": [],
                "diferencias": [],
            }
        

        pagos = list(
            CreditAuditRepository.obtener_pagos(credito)
        )

        capital = dinero(credito.monto)
        movimientos = []
        diferencias = []

        for pago in pagos:
            monto = dinero(pago["monto"])
            mora = dinero(pago["mora"])
            interes = dinero(pago["interes"])
            aporte_capital = dinero(pago["capital"])

            capital_anterior = capital
            capital = dinero(capital - aporte_capital)

            # No asumimos que el remanente sea un excedente
            # válido hasta contrastarlo con AccountStatement.
            total_distribuido = dinero(
                mora + interes + aporte_capital
            )

            diferencia_distribucion = dinero(
                monto - total_distribuido
            )

            if capital < 0:
                diferencias.append({
                    "pago_id": pago["id"],
                    "tipo": "CAPITAL_NEGATIVO",
                    "capital_calculado": capital,
                })

            if diferencia_distribucion < 0:
                diferencias.append({
                    "pago_id": pago["id"],
                    "tipo": "DISTRIBUCION_SUPERA_PAGO",
                    "diferencia": diferencia_distribucion,
                })

            movimientos.append({
                "pago_id": pago["id"],
                "fecha": pago["fecha_emision"],
                "numero_referencia": pago["numero_referencia"],
                "monto": monto,
                "capital_anterior": capital_anterior,
                "mora_pagada": mora,
                "interes_pagado": interes,
                "capital_pagado": aporte_capital,
                "capital_restante": capital,
                "remanente_no_conciliado": (
                    diferencia_distribucion
                ),
            })

        return {
            "credito_id": self.credito_id,
            "capital_original": dinero(credito.monto),
            "capital_final": capital,
            "total_pagos": len(pagos),
            "movimientos": movimientos,
            "diferencias": diferencias,
        }
