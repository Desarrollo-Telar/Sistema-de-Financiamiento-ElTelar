function redondearArriba(valor) {
    return Math.ceil(valor);
}


export class PaymentPlan {
    static contador = 0;

    constructor(credit) {
        PaymentPlan.contador += 1;
        this._no = PaymentPlan.contador;
        this._credit = credit;
        this._estado_pago = this.generarEstado();
        this._plan = [];
        this._plazo = parseInt(this._credit.plazo);
        this._plazo_gracia = parseInt(this._credit.plazo_gracia);
        this._agregar = 0;
    }

    get plazo() {
        return this._plazo;
    }

    get plazoGracia() {
        return this._plazo_gracia;
    }

    generarEstado() {
        return 'VIGENTE';
    }

    get interes() {
        return this._credit.tasaInteres;
    }

    get formaPago() {
        return this._credit.formaDePago;
    }

    get montoInicial() {
        return parseFloat(this._credit.monto).toFixed(2);
    }

    calculoIntereses(dia = null, monto = null) {
        if (monto === null) {
            monto = this.montoInicial;
        }
        const intereses = ((monto * this.interes) );
        const calculo = parseFloat(intereses).toFixed(2);
        return redondearArriba(calculo);
    }

    // Dentro de la clase PaymentPlan

calculoCuota(interes = null, capital = null, mesActual = null) {
    let cuota = 0;
    let plazo = this.plazo;
    let gracia = this.plazoGracia;
    

    if (this.formaPago === 'NIVELADA') {
        const defaultInteres = this.interes;
        const parte1 = (Math.pow(1 + defaultInteres, plazo) * defaultInteres);
        const parte2 = (Math.pow(1 + defaultInteres, plazo) - 1);
        cuota = (parte1 / parte2) * this.montoInicial;
        
    } else if (this.formaPago === 'AMORTIZACIONES A CAPITAL') {
        capital = this.calculoCapital()
        cuota = parseFloat(interes) + parseFloat(capital);

    } else if (this.formaPago === 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO') {
        // Si es el último mes, paga Interés + Todo el Capital
        if (mesActual > gracia) {
            plazo -= gracia;
           

            capital = redondearArriba(parseFloat(this.montoInicial / plazo).toFixed(2));
            cuota = parseFloat(interes) + parseFloat(capital);
        } else {
            // Meses intermedios: Solo el interés
            cuota = parseFloat(interes);
        }

    } else if (this.formaPago === 'INTERES Y CAPITAL AL VENCIMIENTO') {
        // Tu lógica específica: Capitalización en gracia y cuota única al final
        if (mesActual > gracia) {
            plazo -= gracia;
           

            capital = redondearArriba(parseFloat(this.montoInicial / plazo).toFixed(2));
           
            cuota = parseFloat(interes) + parseFloat(capital);
            
            

            
           
        } else {
            // Meses previos al vencimiento no hay cuota exigible
            cuota = 0;
        }
    }

    const calculo = parseFloat(cuota + this._agregar).toFixed(2);
    return redondearArriba(calculo);
}

calculoCapital(cuota = null, intereses = null, mesActual = null) {
    let plazo = this.plazo;
    let gracia = this.plazoGracia;

    if (this.formaPago === 'NIVELADA') {
        return redondearArriba(parseFloat(cuota - intereses).toFixed(2));
        
    } else if (this.formaPago === 'AMORTIZACIONES A CAPITAL') {
        return redondearArriba(parseFloat(this.montoInicial / plazo).toFixed(2));

    } else if (this.formaPago === 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO') {
        
        if (mesActual > gracia) {
            plazo -= gracia;
           

            return redondearArriba(parseFloat(this.montoInicial / plazo).toFixed(2));

        } else {
            
            return 0;
        }

    } else if (this.formaPago === 'INTERES Y CAPITAL AL VENCIMIENTO') {
        if (mesActual > gracia) {
            plazo = plazo - gracia

            return redondearArriba(parseFloat(this.montoInicial / plazo).toFixed(2));

        } else {
            
            return 0;
        }
    }
}

    mesInicial() {
        return this._credit.fechaInicio;
    }

    // Ajuste en el método inicial()
inicial() {
    const mesInicial = this.mesInicial();
    const mesFinal = new Date(mesInicial);
    mesFinal.setMonth(mesFinal.getMonth() + 1);
    
    const dicio = {
        mes: 1,
        fecha_inicio: mesInicial,
        fecha_final: mesFinal,
        monto_prestado: this.montoInicial,
        monto_interes: this.montoInicial
    };

    const intereses = this.calculoIntereses(null, this.montoInicial);
    // Agregamos el parámetro del mes actual (1)
    const cuota = this.calculoCuota(intereses, null, 1);
    const capital = this.calculoCapital(cuota, intereses, 1);

    dicio.intereses = intereses;
    dicio.capital = capital;
    dicio.cuota = cuota;
    return dicio;
}

// Ajuste en el loop de generarPlan()
generarPlan() {
    // Limpiamos el plan antes de empezar
    this._plan = [];
    const primeraCuota = this.inicial();
    this._plan.push(primeraCuota);
    let plazo = this.plazo;
    let gracia = this.plazoGracia;

    for (let mes = 2; mes <= this.plazo; mes++) {
        const anterior = this._plan[this._plan.length - 1];
        let montoParaInteres = 0;

        // 1. LÓGICA DE SALDOS SEGÚN FORMA DE PAGO
        if (this.formaPago === 'INTERES Y CAPITAL AL VENCIMIENTO') {
            // CAPITALIZACIÓN: El nuevo monto es el anterior + los intereses que no se pagaron
            montoParaInteres = parseFloat(anterior.monto_interes) + parseFloat(anterior.intereses);
            
          
            
        } 
        else if (this.formaPago === 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO') {
            // Se mantiene el monto inicial porque el interés se paga mes a mes
            montoParaInteres = parseFloat(anterior.monto_prestado) - parseFloat(anterior.capital);
        } 
        else {
            // NIVELADA o AMORTIZACIÓN CONSTANTE: Se resta el capital ya pagado
            montoParaInteres = parseFloat(anterior.monto_prestado) - parseFloat(anterior.capital);
        }

        let montoOtorgado = parseFloat(anterior.monto_prestado) - parseFloat(anterior.capital);

        // 2. FECHAS
        const mesInicial = new Date(anterior.fecha_final);
        const mesFinal = new Date(mesInicial);
        mesFinal.setMonth(mesFinal.getMonth() + 1);

        // 3. CÁLCULOS DEL MES ACTUAL
        // Importante: calculoIntereses debe recibir el monto capitalizado
        const intereses = this.calculoIntereses(null, montoParaInteres);
        
        // La cuota y el capital necesitan saber el mes actual para decidir si es el vencimiento
        const cuota = this.calculoCuota(intereses, null, mes);
        const capital = this.calculoCapital(cuota, intereses, mes);

        this._plan.push({
            mes: mes,
            fecha_inicio: mesInicial,
            fecha_final: mesFinal,
            monto_prestado: parseFloat(montoOtorgado).toFixed(2), // Aquí se ve el aumento
            monto_interes: parseFloat(montoParaInteres).toFixed(2),
            intereses: intereses,
            capital: capital,
            cuota: cuota
        });
    }

    return this._plan;
}

    recalcular_capital(){
        let total_cap = 0;
        let total_monto = this._credit.monto;
        let plan = this.generarPlan();
        plan.forEach(element => {
            total_cap += element['capital'];
        });
        let diferencia = total_monto - total_cap;
        if (diferencia > 0){
            let promedio = diferencia /this.plazo
            this._plan.length = 0;
            this._agregar = parseFloat(promedio).toFixed(2);
            plan = this.generarPlan();




        }
        return this._plan
            


    }
}
