export class Direccion {
    #street;
    #number;
    #city;
    #state;
    #postal_code;
    #country;
    #type_address;

    constructor(street='', number='', city='', state='', postal_code='', country='', type_address='') {
        this.#street = street;
        this.#number = number;
        this.#city = city;
        this.#state = state;
        this.#postal_code = postal_code;
        this.#country = country;
        this.#type_address = type_address;
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

    // Setters
    set street(value) {
        this.#street = value;
    }

    set number(value) {
        this.#number = value;
    }

    set city(value) {
        this.#city = value;
    }

    set state(value) {
        this.#state = value;
    }

    set postal_code(value) {
        this.#postal_code = value;
    }

    set country(value) {
        this.#country = value;
    }

    set type_address(value) {
        this.#type_address = value;
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
            Type Address: ${this.#type_address}
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
            type_address: this.#type_address
        };
    }
}

export default Direccion;
