export class PaymentPlan {
    static contador = 0;

    constructor(credit) {
        PaymentPlan.contador += 1;
        this._no = PaymentPlan.contador;
        this._credit = credit;
        this._estado_pago = this.generarEstado();
        this._plan = [];
        this._plazo = parseInt(this._credit.plazo);
    }

    get plazo() {
        return this._plazo;
    }

    generarEstado() {
        return 'VIGENTE';
    }

    get interes() {
        return this._credit.tasa_interes;
    }

    get formaPago() {
        return this._credit.forma_de_pago;
    }

    get montoInicial() {
        return parseFloat(this._credit.monto).toFixed(2);
    }

    calculoIntereses(dia = null, monto = null) {
        if (monto === null) {
            monto = this.montoInicial;
        }
        const intereses = ((monto * this.interes) / 365) * dia;
        return parseFloat(intereses).toFixed(2);
    }

    calculoCuota(interes = null, capital = null) {
        let cuota;
        if (this.formaPago === 'NIVELADA') {
            const defaultInteres = this.interes / 12;
            const parte1 = (Math.pow(1 + defaultInteres, this.plazo) * defaultInteres);
            const parte2 = (Math.pow(1 + defaultInteres, this.plazo) - 1);
            cuota = (parte1 / parte2) * this.montoInicial;
        } else {
            cuota = interes + capital;
        }
        return parseFloat(cuota).toFixed(2);
    }

    calculoCapital(cuota = null, intereses = null) {
        if (this.formaPago === 'NIVELADA') {
            return parseFloat(cuota - intereses).toFixed(2);
        } else {
            return parseFloat(this.montoInicial / this.plazo).toFixed(2);
        }
    }

    mesInicial() {
        return this._credit.fecha_inicio;
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

        for (let mes = 2; mes <= this.plazo; mes++) {
            const anterior = plan[plan.length - 1];
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

            plan.push(dicio);
        }

        return plan;
    }
}
