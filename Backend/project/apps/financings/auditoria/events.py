
from datetime import date, timedelta
from decimal import Decimal


class CreditAuditEvents:

    def __init__(self, motor):
        self.motor = motor
        self.eventos = []

    def registrar_vencimiento(self, fecha, descripcion="VENCIMIENTO"):
        interes = self.motor.generar_interes()

        evento = {
            "fecha": fecha,
            "tipo": descripcion,
            "interes_generado": interes,
            "saldo_capital": self.motor.capital,
        }

        self.eventos.append(evento)
        return evento

    def registrar_fecha_limite(self, fecha):
        mora = self.motor.generar_mora()

        evento = {
            "fecha": fecha,
            "tipo": "FECHA_LIMITE",
            "mora_generada": mora,
            "interes_pendiente": self.motor.interes_pendiente,
        }

        self.eventos.append(evento)
        return evento

    def registrar_pago(self, fecha, monto):
        resultado = self.motor.aplicar_pago(monto)

        evento = {
            "fecha": fecha,
            "tipo": "PAGO",
            "monto": Decimal(str(monto)),
            **resultado,
        }

        self.eventos.append(evento)
        return evento

    def obtener_historial(self):
        return sorted(
            self.eventos,
            key=lambda evento: evento["fecha"]
        )
