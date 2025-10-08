
def procesos_de_pago(self, saldo_pendiente, interes, mora):
    monto_depositado = self.monto

    pagado_mora = 0
    pagado_interes = 0
    aporte_capital = 0


    def procesar_pago(tipo, monto_requerido):
        
        nonlocal monto_depositado, pagado_mora, pagado_interes

        if monto_depositado >= monto_requerido:
            monto_depositado = round(monto_depositado - monto_requerido, 2)
                    
            if tipo == 'Mora':
                pagado_mora += monto_requerido
            elif tipo == 'Interes':
                pagado_interes += monto_requerido

            return 0
        else:
            saldo = round(monto_requerido - monto_depositado, 2)
                    
            if tipo == 'Mora':
                pagado_mora += monto_depositado

            elif tipo == 'Interes':
                pagado_interes += monto_depositado

            monto_depositado = 0    
            return saldo
    
     # Procesar pago de mora
    mora = procesar_pago('Mora', mora) 
    if mora > 0:
        aporte_capital = monto_depositado       
        self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
        return f"Pago realizado parcialmente. Quedan Q{mora} de mora pendiente. "

       
    # Procesar pago de intereses
    interes = procesar_pago('Interes', interes)
        
    if interes > 0:
        aporte_capital = monto_depositado
        self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente)
        return f"Pago realizado parcialmente. Quedan Q{interes} de intereses pendientes. "
    
    aporte_capital = monto_depositado
    excedente = None
    saldo_pendiente_antes = saldo_pendiente

    saldo_pendiente -= aporte_capital
    

    if saldo_pendiente < 0:
        excedente = saldo_pendiente
        saldo_pendiente = 0
        aporte_capital = saldo_pendiente_antes
        

    self._registrar_pago(pagado_mora=pagado_mora, pagado_interes=pagado_interes,aporte_capital=aporte_capital,saldo_pendiente=saldo_pendiente, excedente=excedente)
    return f"Pago realizado con éxito. Q{self.monto} restante. Saldo pendiente total: Q{saldo_pendiente}"