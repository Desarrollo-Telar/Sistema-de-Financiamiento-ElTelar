
from decimal import Decimal, ROUND_HALF_UP


CENTAVO = Decimal("0.01")


def dinero(valor):
    return Decimal(str(valor)).quantize(
        CENTAVO,
        rounding=ROUND_HALF_UP
    )


class CreditAuditEngine:

    def __init__(self, capital, tasa_interes, tasa_mora):
        self.capital = dinero(capital)
        self.tasa_interes = Decimal(str(tasa_interes))
        self.tasa_mora = Decimal(str(tasa_mora))

        self.interes_pendiente = Decimal("0.00")
        self.mora_pendiente = Decimal("0.00")

        self.movimientos = []

    def generar_interes(self):
        interes = dinero(
            self.capital * self.tasa_interes
        )

        self.interes_pendiente += interes
        return interes

    def generar_mora(self):
        mora = dinero(
            self.interes_pendiente * self.tasa_mora
        )

        self.mora_pendiente += mora
        return mora

    def aplicar_pago(self, monto):
        restante = dinero(monto)

        pagado_mora = min(
            restante, self.mora_pendiente
        )
        restante -= pagado_mora
        self.mora_pendiente -= pagado_mora

        pagado_interes = min(
            restante, self.interes_pendiente
        )
        restante -= pagado_interes
        self.interes_pendiente -= pagado_interes

        pagado_capital = min(
            restante, self.capital
        )
        restante -= pagado_capital
        self.capital -= pagado_capital

        movimiento = {
            "mora_pagada": pagado_mora,
            "interes_pagado": pagado_interes,
            "capital_pagado": pagado_capital,
            "excedente": restante,
            "saldo_capital": self.capital,
            "interes_pendiente": self.interes_pendiente,
            "mora_pendiente": self.mora_pendiente,
        }

        self.movimientos.append(movimiento)
        return movimiento
