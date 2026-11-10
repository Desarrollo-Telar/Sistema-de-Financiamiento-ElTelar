from decimal import Decimal

from .engine import dinero


class CreditInterestLedger:
    """
    Libro mayor independiente de intereses simples.

    - Los intereses se calculan sobre el capital pendiente.
    - Los intereses impagos se acumulan.
    - No existe capitalización de intereses.
    - Cada período se genera una sola vez.
    - No modifica registros de la base de datos.
    """

    def __init__(self, capital_inicial, tasa_mensual):
        self.capital = dinero(capital_inicial)
        self.tasa_mensual = Decimal(str(tasa_mensual))
        self.interes_pendiente = dinero(0)

        self.periodos_generados = set()
        self.movimientos = []

        if self.capital < 0:
            raise ValueError("El capital inicial no puede ser negativo.")

        if self.tasa_mensual < 0:
            raise ValueError("La tasa mensual no puede ser negativa.")

    def generar_interes(self, periodo, fecha=None):
        """
        Genera intereses sobre el capital vigente.

        periodo: identificador único del período, por ejemplo
                 el ID de PaymentPlan.
        """

        if periodo in self.periodos_generados:
            raise ValueError(
                f"El interés del período {periodo} ya fue generado."
            )

        capital_base = self.capital

        interes_generado = dinero(
            capital_base * self.tasa_mensual
        )

        self.interes_pendiente = dinero(
            self.interes_pendiente + interes_generado
        )

        self.periodos_generados.add(periodo)

        self.movimientos.append({
            "tipo": "INTERES_GENERADO",
            "periodo": periodo,
            "fecha": fecha,
            "capital_base": capital_base,
            "interes_generado": interes_generado,
            "interes_pendiente": self.interes_pendiente,
        })

        return interes_generado

    def registrar_pago(self, pago_id, monto, fecha=None):
        """
        Aplica un pago bajo la prioridad:
        interés -> capital.

        Esta es una versión sin mora. Cuando integremos
        mora utilizaremos AuditPaymentAllocator.
        """

        monto = dinero(monto)

        if monto < 0:
            raise ValueError("El pago no puede ser negativo.")

        interes_pagado = min(
            monto,
            self.interes_pendiente
        )

        disponible = dinero(monto - interes_pagado)

        capital_pagado = min(
            disponible,
            self.capital
        )

        excedente = dinero(disponible - capital_pagado)

        self.interes_pendiente = dinero(
            self.interes_pendiente - interes_pagado
        )

        self.capital = dinero(
            self.capital - capital_pagado
        )

        movimiento = {
            "tipo": "PAGO",
            "pago_id": pago_id,
            "fecha": fecha,
            "monto": monto,
            "interes_pagado": interes_pagado,
            "capital_pagado": capital_pagado,
            "excedente": excedente,
            "capital_restante": self.capital,
            "interes_pendiente": self.interes_pendiente,
        }

        self.movimientos.append(movimiento)

        return movimiento

    def obtener_estado(self):
        return {
            "capital_pendiente": self.capital,
            "interes_pendiente": self.interes_pendiente,
            "periodos_generados": len(self.periodos_generados),
            "movimientos": self.movimientos,
        }