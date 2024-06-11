export class OtraInformacionLaboral {
    #source_of_income;
    #nit;
    #phone_number;
    #customer_id;

    constructor(source_of_income='', nit='', phone_number='', customer_id = '') {
        this.#source_of_income = source_of_income;
        this.#nit = nit;
        this.#phone_number = phone_number;
        this.#customer_id = customer_id;
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

    get customer_id(){
        return this.#customer_id;
    }

    // Setters
    set source_of_income(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la Fuente de Ingreso del cliente');
            throw new Error('Debe ingresar la Fuente de Ingreso del cliente');
        }

        this.#source_of_income = value.trim();
    }

    set nit(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de NIT de la Fuente de Ingreso del cliente');
            throw new Error('Debe ingresar el numero de NIT de la Fuente de Ingreso del cliente');
        }

        this.#nit = value.trim();
        
    }

    set phone_number(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de telefono de la Fuente de Ingreso del cliente');
            throw new Error('Debe ingresar el numero de telefono de la Fuente de Ingreso del cliente');
        }
        // Expresión regular para exactamente 8 dígitos
        const regex = /^\d{8}$/;

        // Validar el formato del número de teléfono
        if (!regex.test(value)) {
            console.error('Numero de telefono no valido, no cumple con el estandar de un numero de telefono. Verificar!!!')
            throw new Error('Número de teléfono no válido. Debe contener exactamente 8 dígitos.');
        }
        
        this.#phone_number = value.trim();
    }

    set customer_id(value){
        this.#customer_id = value;
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `OtraInformacionLaboral {
            Source of Income: ${this.#source_of_income},
            NIT: ${this.#nit},
            Phone Number: ${this.#phone_number},
            Cliente: ${this.#customer_id}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            source_of_income: this.#source_of_income,
            nit: this.#nit,
            phone_number: this.#phone_number,
            customer_id:this.#customer_id
        };
    }
}

export default OtraInformacionLaboral;
