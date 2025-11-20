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
        this._agregar = 0;
    }

    get plazo() {
        return this._plazo;
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

    calculoCuota(interes = null, capital = null) {
        let cuota = 0;
        let capi = parseFloat(capital);
        if (this.formaPago === 'NIVELADA') {
            const defaultInteres = this.interes;
            const parte1 = (Math.pow(1 + defaultInteres, this.plazo) * defaultInteres);
            const parte2 = (Math.pow(1 + defaultInteres, this.plazo) - 1);
            cuota = (parte1 / parte2) * this.montoInicial;
        } else if (this.formaPago === 'AMORTIZACIONES A CAPITAL'){

            cuota = parseFloat(interes) + parseFloat(capi);
            
        }
       
        
        const calculo = parseFloat(cuota+this._agregar).toFixed(2);
        return redondearArriba(calculo);
    }

    calculoCapital(cuota = null, intereses = null) {
        if (this.formaPago === 'NIVELADA') {
            const calculo = parseFloat(cuota - intereses).toFixed(2);
            return redondearArriba(calculo);
        } else {
            const calculo = parseFloat(this.montoInicial / this.plazo).toFixed(2);
            return redondearArriba(calculo);
        }
    }

    mesInicial() {
        return this._credit.fechaInicio;
    }

    inicial() {
        const mesInicial = this.mesInicial();
        const mesFinal = new Date(mesInicial);
        mesFinal.setMonth(mesFinal.getMonth() + 1);
        const diasDiferencia = (mesFinal - mesInicial) / (1000 * 60 * 60 * 24);

        const dicio = {
            mes: 1,
            fecha_inicio: mesInicial,
            fecha_final: mesFinal,
            monto_prestado: this.montoInicial
        };
        const intereses = this.calculoIntereses(diasDiferencia, this.montoInicial);
        let cuota, capital;
        if (this.formaPago === 'NIVELADA') {
            cuota = this.calculoCuota();
            capital = this.calculoCapital(cuota, intereses);
        } else {
            capital = this.calculoCapital();
            
            cuota = this.calculoCuota(intereses, capital);
        }
        dicio.intereses = intereses;
        dicio.capital = capital;
        dicio.cuota = cuota;

        return dicio;
    }

    generarPlan() {
        const plan = [this.inicial()];
        this._plan.push(this.inicial())

        for (let mes = 2; mes <= this.plazo; mes++) {
            const anterior = this._plan[this._plan.length - 1];
            const montoPrestado = parseFloat(anterior.monto_prestado - anterior.capital).toFixed(2);

            const mesInicial = anterior.fecha_final;
            const mesFinal = new Date(mesInicial);
            mesFinal.setMonth(mesFinal.getMonth() + 1);
            const diasDiferencia = (mesFinal - mesInicial) / (1000 * 60 * 60 * 24);

            const intereses = this.calculoIntereses(diasDiferencia, montoPrestado);

            const dicio = {
                mes: mes,
                fecha_inicio: mesInicial,
                fecha_final: mesFinal,
                monto_prestado: montoPrestado,
                intereses: intereses
            };

            let cuota, capital;
            if (this.formaPago === 'NIVELADA') {
                cuota = this.calculoCuota();
                capital = this.calculoCapital(cuota, intereses);
            } else {
                capital = parseFloat(anterior.capital).toFixed(2);

                cuota = this.calculoCuota(intereses, capital);
            }
            dicio.capital = capital;
            dicio.cuota = cuota;

            this._plan.push(dicio);
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
