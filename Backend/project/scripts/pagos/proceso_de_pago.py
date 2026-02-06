def procesos_de_pago(self, saldo_pendiente, interes, mora, capital_generado = 0, tipo_proceso='NORMAL'):
    monto_depositado = self.monto
    
    prioridades = {
        'NORMAL': ['Mora', 'Interes', 'Capital'], # PRIORIDAD CANCELAR LA MOROSIDAD DE LA CUOTA
        'RECUPERACION PARCIAL CAPITAL': ['Capital', 'Interes', 'Mora'], # PRIORIDAD CANCELAR EL CAPITAL DE LA CUOTA GENERADA
        'RECUPERACION TOTAL CAPITAL': ['Capital', 'Interes', 'Mora'], # PRIORIDAD CANCELAR LO MAS ANTES POSIBLE EL SALDO CAPITAL
    }
    
    orden = prioridades.get(tipo_proceso.upper(), prioridades['NORMAL'])
    
    resultados = {
        'pagado_mora': 0,
        'pagado_interes': 0,
        'aporte_capital': 0,
        'pendiente_mora': mora,
        'pendiente_interes': interes,
        'saldo_pendiente_cap': saldo_pendiente,
        'pendiente_capital': capital_generado
    }

    for rubro in orden:
        if monto_depositado <= 0:
            break
            
        if rubro == 'Mora':
            pago = min(monto_depositado, resultados['pendiente_mora'])
            resultados['pagado_mora'] = round(pago, 2)
            resultados['pendiente_mora'] -= pago
            monto_depositado -= pago

        elif rubro == 'Interes':
            pago = min(monto_depositado, resultados['pendiente_interes'])
            resultados['pagado_interes'] = round(pago, 2)
            resultados['pendiente_interes'] -= pago
            monto_depositado -= pago

        elif rubro == 'Capital':
            # Si es RECUPERACIÓN NORMAL, primero cubrimos la cuota de capital generada
            if tipo_proceso == 'RECUPERACION PARCIAL CAPITAL':
                pago = min(monto_depositado, resultados['pendiente_capital'])
            else:
                pago = min(monto_depositado, resultados['saldo_pendiente_cap'])

            resultados['aporte_capital'] += round(pago, 2)
            resultados['saldo_pendiente_cap'] -= pago
            monto_depositado -= pago

    
    # Si después de recorrer el orden aún queda dinero y todavía hay deuda...
    if monto_depositado > 0 and resultados['saldo_pendiente_cap'] > 0:
        # Todo lo que sobre se va a capital hasta dejar la deuda en 0
        pago_extra = min(monto_depositado, resultados['saldo_pendiente_cap'])
        resultados['aporte_capital'] += round(pago_extra, 2)
        resultados['saldo_pendiente_cap'] -= pago_extra
        monto_depositado -= pago_extra

    # Ahora sí, el excedente real es solo si el cliente pagó de más de la deuda total
    excedente = round(monto_depositado, 2) if monto_depositado > 0 else 0
    
    self._registrar_pago(
        pagado_mora=resultados['pagado_mora'],
        pagado_interes=resultados['pagado_interes'],
        aporte_capital=resultados['aporte_capital'],
        saldo_pendiente=resultados['saldo_pendiente_cap'],
        excedente=excedente if excedente > 0 else None
    )

    return self._generar_resumen(resultados, excedente)

def _generar_resumen(self, res, excedente):
    if res['pendiente_mora'] > 0:
        return f"Parcial. Pendiente Mora: Q{res['pendiente_mora']}"
    if res['pendiente_interes'] > 0:
        return f"Parcial. Pendiente Interés: Q{res['pendiente_interes']}"
    return f"Pago procesado. Saldo Cap: Q{res['saldo_pendiente_cap']}. Excedente: Q{excedente}"