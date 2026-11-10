
from decimal import Decimal, ROUND_HALF_UP


CENTAVO = Decimal("0.01")


def dinero(valor):
    return Decimal(str(valor)).quantize(
        CENTAVO,
        rounding=ROUND_HALF_UP
    )


class AuditPaymentAllocator:
    """
    Distribuye pagos sin consultar ni modificar la base de datos.

    Los saldos recibidos deben proceder de la reconstrucción
    independiente, no directamente de PaymentPlan.
    """

    PRIORIDADES = {
        "NORMAL": ("mora", "interes", "capital"),
        "RECUPERACION PARCIAL CAPITAL": (
            "capital", "interes", "mora"
        ),
        "RECUPERACION TOTAL CAPITAL": (
            "capital", "interes", "mora"
        ),
    }

    @classmethod
    def distribuir(
        cls,
        monto,
        saldo_capital,
        interes_pendiente,
        mora_pendiente,
        capital_generado=0,
        tipo_proceso="NORMAL",
    ):
        monto = dinero(monto)

        saldos = {
            "capital": dinero(saldo_capital),
            "interes": dinero(interes_pendiente),
            "mora": dinero(mora_pendiente),
        }

        capital_generado = dinero(capital_generado)
        tipo_proceso = (tipo_proceso or "NORMAL").upper()

        if tipo_proceso not in cls.PRIORIDADES:
            raise ValueError(
                f"Tipo de proceso no reconocido: {tipo_proceso}"
            )

        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")

        if any(valor < 0 for valor in saldos.values()):
            raise ValueError("Los saldos no pueden ser negativos.")

        if capital_generado < 0:
            raise ValueError(
                "El capital generado no puede ser negativo."
            )

        disponible = monto

        pagado = {
            "capital": Decimal("0.00"),
            "interes": Decimal("0.00"),
            "mora": Decimal("0.00"),
        }

        for rubro in cls.PRIORIDADES[tipo_proceso]:
            if disponible <= 0:
                break

            limite = saldos[rubro]

            if (
                rubro == "capital"
                and tipo_proceso == "RECUPERACION PARCIAL CAPITAL"
            ):
                limite = min(limite, capital_generado)

            aplicado = min(disponible, limite)

            pagado[rubro] += aplicado
            saldos[rubro] -= aplicado
            disponible -= aplicado

        # El remanente se aplica a capital, según el
        # comportamiento observado en procesos_de_pago().
        if disponible > 0 and saldos["capital"] > 0:
            aplicado = min(disponible, saldos["capital"])

            pagado["capital"] += aplicado
            saldos["capital"] -= aplicado
            disponible -= aplicado

        resultado = {
            "tipo_proceso": tipo_proceso,
            "monto": monto,
            "pagado_mora": pagado["mora"],
            "pagado_interes": pagado["interes"],
            "aporte_capital": pagado["capital"],
            "saldo_capital": saldos["capital"],
            "interes_pendiente": saldos["interes"],
            "mora_pendiente": saldos["mora"],
            "excedente": disponible,
        }

        total_aplicado = (
            resultado["pagado_mora"]
            + resultado["pagado_interes"]
            + resultado["aporte_capital"]
            + resultado["excedente"]
        )

        if total_aplicado != monto:
            raise ArithmeticError(
                "La distribución no coincide con el monto."
            )

        return resultado
