class OtraInformacionLaboral {
    #source_of_income;
    #nit;
    #phone_number;

    constructor(source_of_income='', nit='', phone_number='') {
        this.#source_of_income = source_of_income;
        this.#nit = nit;
        this.#phone_number = phone_number;
    }

    // Getters
    get source_of_income() {
        return this.#source_of_income;
    }

    get nit() {
        return this.#nit;
    }

    get phone_number() {
        return this.#phone_number;
    }

    // Setters
    set source_of_income(value) {
        this.#source_of_income = value;
    }

    set nit(value) {
        this.#nit = value;
    }

    set phone_number(value) {
        // Expresión regular para exactamente 8 dígitos
        const regex = /^\d{8}$/;

        // Validar el formato del número de teléfono
        if (!regex.test(value)) {
            console.error('Numero de telefono no valido, no cumple con el estandar de un numero de telefono. Verificar!!!')
            return false;
        }
        
        this.#phone_number = value;
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `OtraInformacionLaboral {
            Source of Income: ${this.#source_of_income},
            NIT: ${this.#nit},
            Phone Number: ${this.#phone_number}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            source_of_income: this.#source_of_income,
            nit: this.#nit,
            phone_number: this.#phone_number
        };
    }
}

export default OtraInformacionLaboral;
