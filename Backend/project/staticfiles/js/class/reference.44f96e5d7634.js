export class Referencia {
    #full_name;
    #phone_number;
    #reference_type;
    #customer_id;

    constructor(full_name = '', phone_number = '', reference_type = '', customer_id = '') {
        this.#full_name = full_name;
        this.#phone_number = phone_number;
        this.#reference_type = reference_type;
        this.#customer_id = customer_id;
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

    get customer_id() {
        return this.#customer_id;
    }

    // Setters
    set full_name(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el nombre completo de la referencia del cliente');
            throw new Error('Debe ingresar el nombre completo de la referencia del cliente');
        }

        this.#full_name = value.trim();
    }

    set phone_number(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de telefono de la referencia del cliente');
            throw new Error('Debe ingresar el numero de telefono de la referencia del cliente');
        }


       

        this.#phone_number = value.trim();
    }

    set reference_type(value) {
        this.#reference_type = value;
    }

    set customer_id(value) {
        this.#customer_id = value;
    }

    // Validar
    validar() {
        if (
            (
                this.#full_name.trim() === '' &&
                this.#phone_number.trim() === '' &&
                this.#reference_type.trim() === '' 
               
            ) ||
            (
                !this.#full_name &&
                !this.#phone_number &&
                !this.#reference_type 
               
            )

        ) {
            return false;
        }
        return true;
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `Referencia {
            Full Name: ${this.#full_name},
            Phone Number: ${this.#phone_number},
            Reference Type: ${this.#reference_type},
            Cliente: ${this.#customer_id}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            full_name: this.#full_name,
            phone_number: this.#phone_number,
            reference_type: this.#reference_type,
            customer_id: this.#customer_id
        };
    }
}

export default Referencia;