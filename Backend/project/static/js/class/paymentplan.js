export class PaymentPlan {
    static contador = 0;

    constructor(credit = '') {
        PaymentPlan.contador += 1;
        this._no = PaymentPlan.contador;
        this._credit = credit;
        this._estado_pago = this.generarEstado();
        this._plan = [];
        this._plazo = parseInt(this._credit.plazo);
    }

    get credit(){
        return this._credit;
    }

    set credit(value){
        this._credit = value;
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
        return Math.round(this._credit.monto * 100) / 100;
    }

    calculoIntereses(monto = this.montoInicial) {
        const intereses = (monto * this.interes) / 12;
        return Math.round(intereses * 100) / 100;
    }

    calculoCuota(interes = null, capital = null) {
        if (this.formaPago === 'NIVELADA') {
            const defaultInteres = this.interes / 12;
            const parte1 = (1 + defaultInteres) ** this.plazo * defaultInteres;
            const parte2 = (1 + defaultInteres) ** this.plazo - 1;
            const cuota = (parte1 / parte2) * this.montoInicial;
            return Math.round(cuota * 100) / 100;
        } else {
            const cuota = interes + capital;
            return Math.round(cuota * 100) / 100;
        }
    }

    calculoCapital(cuota = null, intereses = null) {
        if (this.formaPago === 'NIVELADA') {
            return Math.round((cuota - intereses) * 100) / 100;
        } else {
            return Math.round((this.montoInicial / this.plazo) * 100) / 100;
        }
    }

    mesInicial() {
        return new Date(this._credit.fechaInicio);
    }

    inicial() {
        const mesInicial = this.mesInicial();
        const mesFinal = new Date(mesInicial);
        mesFinal.setMonth(mesFinal.getMonth() + 1);

        const dicio = {
            mes: 1,
            'fecha inicio': mesInicial,
            'fecha final': mesFinal,
            'monto_prestado': this.montoInicial,
        };

        const intereses = this.calculoIntereses(this.montoInicial);
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

        for (let mes = 2; mes <= this.plazo; mes++) {
            const anterior = plan[plan.length - 1];
            const montoPrestado = Math.round((anterior['monto_prestado'] - anterior.capital) * 100) / 100;
            const intereses = this.calculoIntereses(montoPrestado);
            const mesInicial = new Date(anterior['fecha final']);
            const mesFinal = new Date(mesInicial);
            mesFinal.setMonth(mesFinal.getMonth() + 1);

            const dicio = {
                mes: mes,
                'fecha inicio': mesInicial,
                'fecha final': mesFinal,
                'monto_prestado': montoPrestado,
                'intereses': intereses,
            };

            let cuota, capital;

            if (this.formaPago === 'NIVELADA') {
                cuota = this.calculoCuota();
                capital = this.calculoCapital(cuota, intereses);
            } else {
                capital = Math.round(anterior.capital * 100) / 100;
                cuota = this.calculoCuota(intereses, capital);
            }

            dicio.capital = capital;
            dicio.cuota = cuota;

            plan.push(dicio);
        }

        return plan;
    }
}
