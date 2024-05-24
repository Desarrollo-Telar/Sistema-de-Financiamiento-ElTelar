class Referencia {
    #full_name;
    #phone_number;
    #reference_type;

    constructor(full_name='', phone_number='', reference_type='') {
        this.#full_name = full_name;
        this.#phone_number = phone_number;
        this.#reference_type = reference_type;
    }

    // Getters
    get full_name() {
        return this.#full_name;
    }

    get phone_number() {
        return this.#phone_number;
    }

    get reference_type() {
        return this.#reference_type;
    }

    // Setters
    set full_name(value) {
        this.#full_name = value;
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

    set reference_type(value) {
        this.#reference_type = value;
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `Referencia {
            Full Name: ${this.#full_name},
            Phone Number: ${this.#phone_number},
            Reference Type: ${this.#reference_type}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            full_name: this.#full_name,
            phone_number: this.#phone_number,
            reference_type: this.#reference_type
        };
    }
}

export default Referencia;