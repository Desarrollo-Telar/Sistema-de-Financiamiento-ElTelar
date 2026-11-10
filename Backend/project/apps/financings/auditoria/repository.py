
from apps.financings.models import Credit, Payment, PaymentPlan, AccountStatement


class CreditAuditRepository:

    @staticmethod
    def obtener_credito(credito_id):
        return Credit.objects.get(pk=credito_id)

    @staticmethod
    def obtener_pagos(credito):
        return list(
            Payment.objects.filter(
                credit=credito,
                estado_transaccion="COMPLETADO", tipo_pago = 'CREDITO'
            )
            .order_by("fecha_emision", "pk")
            .values(
                "id",
                "fecha_emision",
                "monto",
                "numero_referencia",
                "mora",
                "interes",
                "capital",
            )
        )

    @staticmethod
    def obtener_cuotas(credito):
        return list(
            PaymentPlan.objects.filter(
                credit_id=credito
            )
            .order_by("start_date", "pk")
            .values(
                "id",
                "mes",
                "start_date",
                "due_date",
                "fecha_limite",
                "interest",
                "mora",
                "principal",
                "saldo_pendiente",
                "status",
                "interes_generado",
            )
        )

    
    @staticmethod
    def obtener_estados_cuenta(credito):
        return list(
            AccountStatement.objects.filter(
                credit=credito,
                payment__isnull=False,
                description="PAGO DE CREDITO",
            )
            .order_by("payment__fecha_emision", "pk")
            .values(
                "id",
                "payment_id",
                "interest_paid",
                "late_fee_paid",
                "capital_paid",
                "saldo_pendiente",
                "abono",
                "excedente",
                "numero_referencia",
            )
        )

