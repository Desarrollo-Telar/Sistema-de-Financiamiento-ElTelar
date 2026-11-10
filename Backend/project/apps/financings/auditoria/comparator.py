
from decimal import Decimal

from .engine import dinero
from .repository import CreditAuditRepository


class CreditAuditComparator:
    """
    Auditor de consistencia entre Payment y AccountStatement.

    No modifica registros de la base de datos.
    No recalcula todavía intereses contractuales ni mora.
    """

    def __init__(self):
        self.repo = CreditAuditRepository()

    @staticmethod
    def valor(valor):
        """Normaliza valores monetarios a dos decimales."""
        return dinero(valor if valor is not None else 0)

    def analizar(self, credito_id):
        credito = self.repo.obtener_credito(credito_id)

        pagos = self.repo.obtener_pagos(credito)
        estados = self.repo.obtener_estados_cuenta(credito)

        estados_por_pago = {}

        for estado in estados:
            estados_por_pago.setdefault(
                estado["payment_id"], []
            ).append(estado)

        diferencias = []
        pagos_correctos = 0
        pagos_con_diferencias = 0
        total_excedentes = Decimal("0.00")

        for pago in pagos:
            pago_id = pago["id"]
            errores_iniciales = len(diferencias)

            monto = self.valor(pago["monto"])
            mora = self.valor(pago["mora"])
            interes = self.valor(pago["interes"])
            capital = self.valor(pago["capital"])

            total_distribuido = mora + interes + capital

            registros = estados_por_pago.get(pago_id, [])

            # 1. Verificar existencia y unicidad del estado de cuenta
            if len(registros) != 1:
                diferencias.append({
                    "pago_id": pago_id,
                    "fecha": pago["fecha_emision"],
                    "referencia": pago["numero_referencia"],
                    "tipo": "CANTIDAD_ESTADOS_CUENTA",
                    "esperado": 1,
                    "registrado": len(registros),
                })

                # No podemos justificar el excedente sin
                # un estado de cuenta único y válido.
                pagos_con_diferencias += 1
                continue

            estado = registros[0]

            excedente = self.valor(estado["excedente"])
            total_excedentes += excedente

            # 2. Verificar distribución del pago
            total_justificado = total_distribuido + excedente

            if monto != total_justificado:
                diferencias.append({
                    "pago_id": pago_id,
                    "fecha": pago["fecha_emision"],
                    "referencia": pago["numero_referencia"],
                    "tipo": "DISTRIBUCION_PAGO",
                    "esperado": monto,
                    "registrado": total_justificado,
                    "excedente": excedente,
                    "diferencia": monto - total_justificado,
                })

            # 3. Verificar Payment contra AccountStatement
            campos = [
                ("mora", "late_fee_paid"),
                ("interes", "interest_paid"),
                ("capital", "capital_paid"),
                ("monto", "abono"),
            ]

            for campo_pago, campo_estado in campos:
                valor_pago = self.valor(pago[campo_pago])
                valor_estado = self.valor(estado[campo_estado])

                if valor_pago != valor_estado:
                    diferencias.append({
                        "pago_id": pago_id,
                        "fecha": pago["fecha_emision"],
                        "referencia": pago["numero_referencia"],
                        "tipo": "DIFERENCIA_ESTADO_CUENTA",
                        "campo": campo_estado,
                        "esperado": valor_pago,
                        "registrado": valor_estado,
                        "diferencia": valor_pago - valor_estado,
                    })

            # 4. Verificar que el excedente no sea negativo
            if excedente < 0:
                diferencias.append({
                    "pago_id": pago_id,
                    "fecha": pago["fecha_emision"],
                    "referencia": pago["numero_referencia"],
                    "tipo": "EXCEDENTE_NEGATIVO",
                    "registrado": excedente,
                })

            # 5. Clasificar el resultado del pago
            if len(diferencias) == errores_iniciales:
                pagos_correctos += 1
            else:
                pagos_con_diferencias += 1

        return {
            "credito_id": credito.pk,
            "codigo": str(credito),
            "pagos_analizados": len(pagos),
            "pagos_correctos": pagos_correctos,
            "pagos_con_diferencias": pagos_con_diferencias,
            "total_excedentes": total_excedentes,
            "total_diferencias": len(diferencias),
            "diferencias": diferencias,
        }
