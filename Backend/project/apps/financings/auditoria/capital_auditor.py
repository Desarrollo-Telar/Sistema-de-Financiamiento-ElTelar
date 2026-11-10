
from .engine import dinero
from .repository import CreditAuditRepository


class CapitalAuditor:
    """
    Reconstruye el capital pendiente utilizando los
    pagos registrados y compara cada resultado con
    AccountStatement.

    Solo realiza consultas de lectura.
    """

    def __init__(self):
        self.repo = CreditAuditRepository()

    def analizar(self, credito_id):
        credito = self.repo.obtener_credito(credito_id)
        pagos = self.repo.obtener_pagos(credito)
        estados = self.repo.obtener_estados_cuenta(credito)

        capital_inicial = dinero(credito.monto)
        capital_pendiente = capital_inicial

        estados_por_pago = {}

        for estado in estados:
            estados_por_pago.setdefault(
                estado["payment_id"], []
            ).append(estado)

        movimientos = []
        diferencias = []

        for pago in pagos:
            capital_pagado = dinero(pago["capital"] or 0)
            capital_anterior = capital_pendiente

            capital_pendiente = dinero(
                capital_pendiente - capital_pagado
            )

            registros = estados_por_pago.get(pago["id"], [])

            saldo_registrado = None

            if len(registros) == 1:
                estado = registros[0]

                if estado["saldo_pendiente"] is not None:
                    saldo_registrado = dinero(
                        estado["saldo_pendiente"]
                    )

                    if capital_pendiente != saldo_registrado:
                        diferencias.append({
                            "pago_id": pago["id"],
                            "fecha": pago["fecha_emision"],
                            "tipo": "DIFERENCIA_SALDO_CAPITAL",
                            "calculado": capital_pendiente,
                            "registrado": saldo_registrado,
                            "diferencia": (
                                capital_pendiente
                                - saldo_registrado
                            ),
                        })

            else:
                diferencias.append({
                    "pago_id": pago["id"],
                    "tipo": "ESTADO_CUENTA_NO_UNICO",
                    "cantidad": len(registros),
                })

            if capital_pendiente < 0:
                diferencias.append({
                    "pago_id": pago["id"],
                    "tipo": "CAPITAL_NEGATIVO",
                    "capital_calculado": capital_pendiente,
                })

            movimientos.append({
                "pago_id": pago["id"],
                "fecha": pago["fecha_emision"],
                "referencia": pago["numero_referencia"],
                "capital_anterior": capital_anterior,
                "capital_pagado": capital_pagado,
                "capital_calculado": capital_pendiente,
                "capital_registrado": saldo_registrado,
            })

        return {
            "credito_id": credito.pk,
            "codigo": str(credito),
            "capital_inicial": capital_inicial,
            "capital_final_calculado": capital_pendiente,
            "pagos_analizados": len(pagos),
            "movimientos": movimientos,
            "total_diferencias": len(diferencias),
            "diferencias": diferencias,
        }
