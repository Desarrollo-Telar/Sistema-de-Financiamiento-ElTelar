import {Hipoteca, DerechoDePosesionHipoteca, Fiador, Cheque,Vehiculo,Mobiliaria } from './type_guarantee.js'

export class Guarantee {
    static contador = 0;

    constructor(detalle_garantia, descripcion = null) {
        Guarantee.contador += 1;
        this._count = Guarantee.contador;
        this._description = descripcion;
        this._detalle_garantia = detalle_garantia.map(dg => new DetailGuarantee(dg.tipo_garantia, dg.valor_cobertura, dg.especificacion));
        this._suma_total = this.calcularSumaTotal();
        this._guarantee = {};
    }

    get descripcion() {
        return this._description;
    }

    set descripcion(value) {
        this._description = value;
    }

    get suma_total() {
        return this._suma_total;
    }

    calcularSumaTotal() {
        // Asegúrate de que los valores sean números
        return this._detalle_garantia.reduce((sum, detalle) => sum + parseFloat(detalle.valorCobertura), 0);
    }

    toJSON() {      
        this._guarantee['description'] = this._description;
        this._guarantee['suma_total'] = this._suma_total;
        return JSON.stringify(this._guarantee, null, 4);
    }

    toString() {
        let resultado = `\n\nSuma Total: ${this.suma_total}\n\n\n`;
        this._detalle_garantia.forEach((detalle, index) => {
            resultado += `  Detalle ${index + 1}:\n`;
            resultado += `    Tipo de Garantia: ${detalle.tipoGarantia.constructor.name}\n`;
            resultado += `    Valor Cobertura: ${detalle.valorCobertura}\n`;
            resultado += `    Especificaciones: ${JSON.stringify(detalle.tipoGarantia, null, 4)}\n`;
        });
        return resultado;
    }
}


export class DetailGuarantee {
    static contador = 0;

    constructor(tipo_garantia, valor_cobertura = 0, especificacion = null) {
        DetailGuarantee.contador += 1;
        this._tipo_garantia = this.crearTipoDeGarantia(tipo_garantia, especificacion);
        this._valor_cobertura = parseFloat(valor_cobertura); // Asegúrate de que sea un número
        this._dic = {};
    }

    get tipoGarantia() {
        return this._tipo_garantia;
    }

    get valorCobertura() {
        return this._valor_cobertura;
    }

    crearTipoDeGarantia(tipo_garantia, especificacion) {
        switch (tipo_garantia.toUpperCase()) { // Convertir tipo_garantia a mayúsculas
            case 'HIPOTECA':
                return new Hipoteca(especificacion);
            case 'DERECHO DE POSESION HIPOTECA': // Asegúrate de que el nombre coincida con el uso en el código
                return new DerechoDePosesionHipoteca(especificacion);
            case 'FIADOR':
                return new Fiador(especificacion);
            case 'CHEQUE':
                return new Cheque(especificacion);
            case 'VEHICULO':
                return new Vehiculo(especificacion);
            case 'MOBILIARIA':
                return new Mobiliaria(especificacion);
            default:
                throw new Error(`Tipo de garantía desconocido: ${tipo_garantia}`);
        }
    }

    get diccionario() {
        this._dic['tipo_garantia'] = this._tipo_garantia.diccionario;
        return this._dic;
    }

    toString() {
        return `Tipo de Garantía: ${this._tipo_garantia.constructor.name}, Valor de Cobertura: ${this._valor_cobertura}, Especificaciones: ${JSON.stringify(this._tipo_garantia, null, 4)}`;
    }
}
