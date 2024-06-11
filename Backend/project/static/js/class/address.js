export class Direccion {
    #street;
    #number;
    #city;
    #state;
    #postal_code;
    #country;
    #type_address;
    #customer_id;

    constructor(street = '', number = '', city = '', state = '', postal_code = '', country = '', type_address = '', customer_id = '') {
        this.#street = street;
        this.#number = number;
        this.#city = city;
        this.#state = state;
        this.#postal_code = postal_code;
        this.#country = country;
        this.#type_address = type_address;
        this.#customer_id = customer_id;
    }

    // Getters
    get street() {
        return this.#street;
    }

    get number() {
        return this.#number;
    }

    get city() {
        return this.#city;
    }

    get state() {
        return this.#state;
    }

    get postal_code() {
        return this.#postal_code;
    }

    get country() {
        return this.#country;
    }

    get type_address() {
        return this.#type_address;
    }

    get customer_id() {
        return this.#customer_id;
    }

    // Setters
    set street(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la direccion del cliente');
            throw new Error('Debe ingresar la direccion del cliente');
        }

        this.#street = value.trim();
    }

    set number(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la zona de la direccion del cliente');
            throw new Error('Debe ingresar la zona de la direccion del cliente');
        }

        this.#number = value.trim();
    }

    set city(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la ciudad de la direccion del cliente');
            throw new Error('Debe ingresar la ciudad de la direccion del cliente');
        }

        this.#city = value.trim();
    }

    set state(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el municipio de la direccion del cliente');
            throw new Error('Debe ingresar el municipio de la direccion del cliente');
        }

        this.#state = value.trim();
    }

    set postal_code(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el codigo postal de la direccion del cliente');
            throw new Error('Debe ingresar el codigo postal de la direccion del cliente');
        }

        this.#postal_code = value.trim();
    }

    set country(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el pais de la direccion del cliente');
            throw new Error('Debe ingresar el pais de la direccion del cliente');
        }

        this.#country = value.trim();
    }

    set type_address(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el tipo de direccion del cliente');
            throw new Error('Debe ingresar el tipo de direccion del cliente');
        }

        this.#type_address = value.trim();
    }

    set customer_id(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el nombre del cliente o id de la direccion del cliente');
            throw new Error('Debe ingresar el nombre del cliente o id de la direccion del cliente');
        }

        this.#type_address = value.trim();
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `Direccion {
            Street: ${this.#street},
            Number: ${this.#number},
            City: ${this.#city},
            State: ${this.#state},
            Postal Code: ${this.#postal_code},
            Country: ${this.#country},
            Type Address: ${this.#type_address},
            customer_id: ${this.#customer_id}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            street: this.#street,
            number: this.#number,
            city: this.#city,
            state: this.#state,
            postal_code: this.#postal_code,
            country: this.#country,
            type_address: this.#type_address,
            customer_id: this.#customer_id
        };
    }
}

export default Direccion;
