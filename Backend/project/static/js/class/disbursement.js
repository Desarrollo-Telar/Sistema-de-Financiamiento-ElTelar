export class Desembolso {
    constructor(
        credit_id = 0,
        monto_total_desembolso = 0,
        honorarios = 0,
        poliza_seguro = 0,
        monto_credito = 0,
        saldo_anterior = 0,
        forma_desembolso = 'APLICACIÓN GASTOS'
    ) {
        this._credit_id = credit_id;
        this._monto_total_desembolso = monto_total_desembolso;
        this._honorarios = honorarios;
        this._poliza_seguro = poliza_seguro;
        this._monto_credito = monto_credito;
        this._saldo_anterior = saldo_anterior;
        this._forma_desembolso = forma_desembolso;
    }

    // Métodos get
    get credit_id() {
        return this._credit_id;
    }

    get monto_total_desembolso() {
        return this._monto_total_desembolso;
    }

    get honorarios() {
        return this._honorarios;
    }

    get poliza_seguro() {
        return this._poliza_seguro;
    }

    get monto_credito() {
        return this._monto_credito;
    }

    get saldo_anterior() {
        return this._saldo_anterior;
    }

    get forma_desembolso() {
        return this._forma_desembolso;
    }

    // Métodos set
    set credit_id(value) {
        this._credit_id = value;
    }

    set monto_total_desembolso(value) {
        this._monto_total_desembolso = value;
    }

    set honorarios(value) {
        this._honorarios = value;
    }

    set poliza_seguro(value) {
        this._poliza_seguro = value;
    }

    set monto_credito(value) {
        this._monto_credito = value;
    }

    set saldo_anterior(value) {
        this._saldo_anterior = value;
    }

    set forma_desembolso(value) {
        this._forma_desembolso = value;
    }

    // Método para calcular el total a depositar
    get total_a_depositar() {
        return this._monto_credito - (this._honorarios + this._poliza_seguro + this._saldo_anterior);
    }

    // Método para convertir a JSON
    toJson() {
        return {
            forma_desembolso: this._forma_desembolso,
            monto_credito: this._monto_credito,
            saldo_anterior: this._saldo_anterior,
            honorarios: this._honorarios,
            poliza_seguro: this._poliza_seguro,
            monto_total_desembolso: this.total_a_depositar, // Sin paréntesis
            credit_id: this._credit_id
        };
    }
}
