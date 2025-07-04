export class Credit {
    static contador = 0;
    #id;
    #proposito;
    #monto;
    #plazo;
    #tasa_interes;
    #forma_de_pago;
    #frecuencia_pago;
    #fecha_inicio;
    #fecha_vencimiento;
    #tipo_credito;
    #destino_id;
    #customer_id;

    constructor(proposito = '', monto = '', plazo = '', tasa_interes = '', forma_de_pago = '', frecuencia_pago = '', fecha_inicio = '', tipo_credito = '', destino_id = null, customer_id = '', fecha_vencimiento = null) {
        Credit.contador++;
        this.#id = Credit.contador;
        this.#proposito = proposito;
        this.#monto = parseFloat(monto);
        this.#plazo = parseInt(plazo);
        this.#tasa_interes = parseFloat(tasa_interes);
        this.#forma_de_pago = forma_de_pago;
        this.#frecuencia_pago = frecuencia_pago;
        this.#fecha_inicio = new Date(fecha_inicio);
        this.#fecha_vencimiento = fecha_vencimiento ? new Date(fecha_vencimiento) : this.calcularFechaVencimiento();
        this.#tipo_credito = tipo_credito;
        this.#destino_id = destino_id;
        this.#customer_id = customer_id;
    }

    get proposito() {
        return this.#proposito;
    }

    get monto() {
        return this.#monto;
    }

    get plazo() {
        return this.#plazo;
    }

    get tasaInteres() {
        const tasa = this.#tasa_interes;

        return tasa > 1 ? (tasa / 12)/100 : tasa/12;
    }

    get formaDePago() {
        return this.#forma_de_pago;
    }

    get frecuenciaPago() {
        return this.#frecuencia_pago;
    }

    get fechaInicio() {
        return this.#fecha_inicio;
    }

    get fechaVencimiento() {
        return this.#fecha_vencimiento;
        
    }

    get tipoCredito() {
        if (this.#destino_id) {
            this.#tipo_credito = this.#destino_id.type_of_product_or_service;
        }
        return this.#tipo_credito;
    }

    get destinoId() {
        return this.#destino_id;
    }

    get customerId() {
        return this.#customer_id;
    }

    set proposito(value) {
        this.#proposito = value;
    }

    set monto(value) {
        this.#monto = parseFloat(value);
    }

    set plazo(value) {
        this.#plazo = parseInt(value);
    }

    set tasaInteres(value) {
        this.#tasa_interes = parseFloat(value);
    }

    set formaDePago(value) {
        const formasDePagoValidas = ['NIVELADA', 'AMORTIZACIONES A CAPITAL'];
        if (formasDePagoValidas.includes(value)) {
            this.#forma_de_pago = value;
        } else {
            console.error("Forma de pago no válida");
        }
    }

    set frecuenciaPago(value) {
        const frecuenciasPagoValidas = ['MENSUAL', 'TRIMESTRAL', 'SEMANAL'];
        if (frecuenciasPagoValidas.includes(value)) {
            this.#frecuencia_pago = value;
        } else {
            console.error("Frecuencia de pago no válida");
        }
    }

    set fechaInicio(value) {
        this.#fecha_inicio = new Date(value);
    }

    set fechaVencimiento(value) {
        this.#fecha_vencimiento = new Date(value);
    }

    set tipoCredito(value) {
        const tiposCreditoValidos = ['AGROPECUARIO Y/O PRODUCTIVO', 'COMERCIO', 'SERVICIOS', 'CONSUMO', 'VIVIENDA'];
        if (tiposCreditoValidos.includes(value)) {
            this.#tipo_credito = value;
        } else {
            console.error('Error de tipo de crédito');
        }
    }

    set destinoId(value) {
        this.#destino_id = value;
    }

    set customerId(value) {
        this.#customer_id = value;
    }

    calcularFechaVencimiento() {
        const fechaInicio = this.#fecha_inicio;
        const fechaVencimiento = new Date(fechaInicio);
        fechaVencimiento.setMonth(fechaVencimiento.getMonth() + this.#plazo);
        return fechaVencimiento;
    }

    toJSON() {
        return {
            proposito: this.#proposito,
            monto: this.#monto,
            plazo: this.#plazo,
            tasa_interes: this.#tasa_interes,
            forma_de_pago: this.#forma_de_pago,
            frecuencia_pago: this.#frecuencia_pago,
            fecha_inicio: this.#fecha_inicio,
            fecha_vencimiento: this.#fecha_vencimiento,
            tipo_credito: this.#tipo_credito,
            destino_id: this.#destino_id,
            customer_id: this.#customer_id,
        };
    }

    toString() {
        return `Credito: \nID: ${this.#id},\nFecha Inicio: ${this.fechaInicio.toISOString().split('T')[0]},\nPlazo: ${this.#plazo} meses,\nFecha de Vencimiento: ${this.fechaVencimiento.toISOString().split('T')[0]},\nFiador: ${this.#customer_id.nombre} ${this.#customer_id.apellido}`;
    }
}
