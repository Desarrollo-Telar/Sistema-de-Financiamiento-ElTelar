
from datetime import datetime, date

from .engine import dinero
from .repository import CreditAuditRepository
from .interest_ledger import CreditInterestLedger


class CreditChronologicalAuditor:
    """
    Reconstrucción cronológica experimental de un crédito.

    Funcionalidades:
    - Consulta el crédito, las cuotas y los pagos.
    - Reconstruye intereses simples sobre capital pendiente.
    - Acumula intereses que no han sido pagados.
    - Procesa los pagos en orden cronológico.
    - Compara intereses y capital calculados con los registrados.
    - Permite establecer una fecha de corte histórica.
    - Excluye vencimientos y pagos posteriores a la fecha de corte.
    - No modifica información de la base de datos.

    Limitaciones:
    - No calcula mora.
    - No considera condiciones especiales de interés.
    - No reconstruye cambios históricos en las condiciones del crédito.
    - No debe utilizarse todavía para declarar errores financieros.
    """

    def __init__(self, credito_id, fecha_corte=None):
        self.credito_id = credito_id

        self.fecha_corte = (
            self.normalizar_fecha(fecha_corte)
            if fecha_corte is not None
            else date.today()
        )

    @staticmethod
    def normalizar_fecha(valor):
        """
        Convierte un datetime a date o conserva un date.

        Se utiliza para comparar las fechas de los pagos,
        vencimientos y fecha de corte.
        """

        if isinstance(valor, datetime):
            return valor.date()

        if isinstance(valor, date):
            return valor

        raise ValueError(
            f"Fecha no válida: {valor!r}"
        )

    def ejecutar(self):
        """
        Ejecuta la simulación cronológica del crédito.
        """

        # --------------------------------------------------
        # 1. OBTENER INFORMACIÓN DEL CRÉDITO
        # --------------------------------------------------

        credito = CreditAuditRepository.obtener_credito(
            self.credito_id
        )

        tipo_proceso = (
            credito.tipo_proceso or ""
        ).strip().upper()

        # Los procesos extraordinarios se revisan manualmente.
        if tipo_proceso != "NORMAL":
            return {
                "credito_id": self.credito_id,
                "fecha_corte": self.fecha_corte,
                "estado": "REVISION_MANUAL",
                "motivo": (
                    "El crédito utiliza un tipo de proceso "
                    f"no admitido para auditoría automática: "
                    f"{tipo_proceso or 'NO DEFINIDO'}"
                ),
                "eventos": [],
                "capital_final_simulado": None,
                "interes_pendiente_simulado": None,
            }

        # --------------------------------------------------
        # 2. OBTENER CUOTAS Y PAGOS
        # --------------------------------------------------

        cuotas = list(
            CreditAuditRepository.obtener_cuotas(
                credito
            )
        )

        pagos = list(
            CreditAuditRepository.obtener_pagos(
                credito
            )
        )

        # --------------------------------------------------
        # 3. INICIALIZAR LIBRO MAYOR INDEPENDIENTE
        # --------------------------------------------------

        ledger = CreditInterestLedger(
            capital_inicial=credito.monto,
            tasa_mensual=credito.tasa_interes
        )

        # --------------------------------------------------
        # 4. CONSTRUIR EVENTOS CRONOLÓGICOS
        # --------------------------------------------------

        eventos = []

        # Eventos de vencimiento de cuotas.
        for cuota in cuotas:

            fecha_vencimiento = self.normalizar_fecha(
                cuota["due_date"]
            )

            eventos.append({
                "tipo": "VENCIMIENTO",
                "fecha": fecha_vencimiento,
                "orden": 0,
                "id": cuota["id"],
                "cuota": cuota,
            })

        # Eventos de pagos realizados.
        for pago in pagos:

            fecha_pago = self.normalizar_fecha(
                pago["fecha_emision"]
            )

            eventos.append({
                "tipo": "PAGO",
                "fecha": fecha_pago,
                "orden": 1,
                "id": pago["id"],
                "pago": pago,
            })

        # --------------------------------------------------
        # 5. ORDENAR LOS EVENTOS
        # --------------------------------------------------

        # En la misma fecha:
        # 1. Se procesa el vencimiento.
        # 2. Se procesa el pago.
        #
        # Los pagos de un mismo día se ordenan por ID.
        #
        # Este orden es una hipótesis de simulación y debe
        # validarse contra las reglas operativas del sistema.

        eventos.sort(
            key=lambda evento: (
                evento["fecha"],
                evento["orden"],
                evento["id"]
            )
        )

        # --------------------------------------------------
        # 6. APLICAR FECHA DE CORTE
        # --------------------------------------------------

        # Se excluyen todos los eventos posteriores a
        # la fecha de corte indicada.

        eventos = [
            evento
            for evento in eventos
            if evento["fecha"] <= self.fecha_corte
        ]

        # --------------------------------------------------
        # 7. PROCESAR LOS EVENTOS
        # --------------------------------------------------

        resultados = []

        for evento in eventos:

            # ==============================================
            # EVENTO: VENCIMIENTO DE CUOTA
            # ==============================================

            if evento["tipo"] == "VENCIMIENTO":

                capital_base = ledger.capital

                interes_generado = ledger.generar_interes(
                    periodo=evento["id"],
                    fecha=evento["fecha"]
                )

                resultados.append({
                    "tipo": "INTERES_GENERADO",
                    "fecha": evento["fecha"],
                    "cuota_id": evento["id"],
                    "capital_base": capital_base,
                    "interes_calculado": interes_generado,
                    "interes_pendiente": (
                        ledger.interes_pendiente
                    ),
                })

            # ==============================================
            # EVENTO: PAGO REALIZADO
            # ==============================================

            elif evento["tipo"] == "PAGO":

                pago = evento["pago"]

                resultado_pago = ledger.registrar_pago(
                    pago_id=pago["id"],
                    monto=pago["monto"],
                    fecha=evento["fecha"]
                )

                interes_calculado = dinero(
                    resultado_pago["interes_pagado"]
                )

                interes_registrado = dinero(
                    pago["interes"]
                )

                capital_calculado = dinero(
                    resultado_pago["capital_pagado"]
                )

                capital_registrado = dinero(
                    pago["capital"]
                )

                diferencia_interes = dinero(
                    interes_calculado - interes_registrado
                )

                diferencia_capital = dinero(
                    capital_calculado - capital_registrado
                )

                resultados.append({
                    "tipo": "PAGO",
                    "fecha": evento["fecha"],
                    "pago_id": pago["id"],
                    "numero_referencia": pago.get(
                        "numero_referencia"
                    ),
                    "monto": dinero(pago["monto"]),

                    # Distribución independiente
                    "interes_calculado": interes_calculado,
                    "capital_calculado": capital_calculado,

                    # Distribución registrada
                    "interes_registrado": interes_registrado,
                    "capital_registrado": capital_registrado,

                    # Diferencias matemáticas
                    "diferencia_interes": diferencia_interes,
                    "diferencia_capital": diferencia_capital,

                    # Estado del libro mayor
                    "capital_restante": dinero(
                        resultado_pago["capital_restante"]
                    ),
                    "interes_pendiente": dinero(
                        resultado_pago["interes_pendiente"]
                    ),
                    "excedente_simulado": dinero(
                        resultado_pago["excedente"]
                    ),
                })

        # --------------------------------------------------
        # 8. RESUMEN DE DIFERENCIAS
        # --------------------------------------------------

        diferencias = []

        for movimiento in resultados:

            if movimiento["tipo"] != "PAGO":
                continue

            if (
                movimiento["diferencia_interes"] != 0
                or movimiento["diferencia_capital"] != 0
            ):
                diferencias.append({
                    "pago_id": movimiento["pago_id"],
                    "fecha": movimiento["fecha"],
                    "diferencia_interes": (
                        movimiento["diferencia_interes"]
                    ),
                    "diferencia_capital": (
                        movimiento["diferencia_capital"]
                    ),
                    "clasificacion": (
                        "DIFERENCIA_EN_SIMULACION"
                    ),
                })

        # --------------------------------------------------
        # 9. DEVOLVER RESULTADO
        # --------------------------------------------------

        return {
            "credito_id": self.credito_id,
            "estado": "SIMULACION",
            "fecha_corte": self.fecha_corte,
            "tipo_proceso": tipo_proceso,
            "forma_de_pago": credito.forma_de_pago,
            "capital_original": dinero(credito.monto),
            "tasa_mensual": credito.tasa_interes,
            "total_cuotas": len(cuotas),
            "total_pagos": len(pagos),
            "eventos_procesados": len(resultados),
            "eventos": resultados,
            "capital_final_simulado": dinero(
                ledger.capital
            ),
            "interes_pendiente_simulado": dinero(
                ledger.interes_pendiente
            ),
            "total_diferencias": len(diferencias),
            "diferencias": diferencias,
        }
