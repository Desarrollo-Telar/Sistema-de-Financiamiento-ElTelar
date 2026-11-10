
from datetime import date, datetime, timedelta

from .engine import CreditAuditEngine
from .events import CreditAuditEvents


class CreditAuditReconstructor:

    def __init__(self, capital, tasa_interes, tasa_mora):
        self.motor = CreditAuditEngine(
            capital=capital,
            tasa_interes=tasa_interes,
            tasa_mora=tasa_mora,
        )
        self.eventos = CreditAuditEvents(self.motor)

    @staticmethod
    def normalizar_fecha(valor):
        if isinstance(valor, datetime):
            return valor.date()
        return valor

    def reconstruir(self, vencimientos, pagos, fecha_corte=None):
        """
        vencimientos: lista de fechas de vencimiento.
        pagos: lista de diccionarios:
            {"fecha": date(...), "monto": "500"}

        fecha_corte: fecha hasta la que se reconstruye.
        """
        operaciones = []

        for fecha in vencimientos:
            fecha = self.normalizar_fecha(fecha)

            operaciones.append({
                "fecha": fecha,
                "prioridad": 0,
                "tipo": "VENCIMIENTO",
            })

            operaciones.append({
                "fecha": fecha + timedelta(days=16),
                "prioridad": 2,
                "tipo": "FECHA_LIMITE",
            })

        for indice, pago in enumerate(pagos):
            operaciones.append({
                "fecha": self.normalizar_fecha(pago["fecha"]),
                "prioridad": 1,
                "tipo": "PAGO",
                "monto": pago["monto"],
                "indice": indice,
            })

        operaciones.sort(
            key=lambda op: (
                op["fecha"],
                op["prioridad"],
                op.get("indice", 0),
            )
        )

        for operacion in operaciones:
            fecha = operacion["fecha"]

            if fecha_corte is not None:
                if fecha > self.normalizar_fecha(fecha_corte):
                    continue

            if operacion["tipo"] == "VENCIMIENTO":
                self.eventos.registrar_vencimiento(fecha)

            elif operacion["tipo"] == "FECHA_LIMITE":
                # El motor genera mora sobre el interés
                # pendiente al comenzar el día 16 posterior.
                self.eventos.registrar_fecha_limite(fecha)

            elif operacion["tipo"] == "PAGO":
                self.eventos.registrar_pago(
                    fecha,
                    operacion["monto"],
                )

        return {
            "capital": self.motor.capital,
            "interes_pendiente": self.motor.interes_pendiente,
            "mora_pendiente": self.motor.mora_pendiente,
            "historial": self.eventos.obtener_historial(),
        }
