export class Direccion {
    #street;
    #number;
    #city;
    #state;
 
    #country;
    #type_address;
    #customer_id;
    #longitud;
    #latitud;

    constructor(street = '', number = '', city = '', state = '',  country = '', type_address = '', customer_id = '',longitud='',latitud='') {
        this.#street = street;
        this.#number = number;
        this.#city = city;
        this.#state = state;
      
        this.#country = country;
        this.#type_address = type_address;
        this.#customer_id = customer_id;
        this.#latitud = latitud;
        this.#longitud= longitud;
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

    

    get country() {
        return this.#country;
    }

    get type_address() {
        return this.#type_address;
    }

    get customer_id() {
        return this.#customer_id;
    }

    get latitud(){
        return this.#latitud;
    }

    get longitud(){
        return this.#longitud;
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
       

        this.#customer_id = value;
    }

    set latitud(value){
        this.#latitud = value;
    }

    set longitud(value){
        this.#longitud = value;
    }

    // Metodo para validar que todos los campos esten ingresados
    validar() {
        if (
            (this.#street.trim() === '' && this.#number.trim() === '' && this.#city.trim() === '' && this.#state.trim() === '' && this.#country.trim() === '' && this.#type_address.trim() === '' ) ||
            (!this.#street && !this.#number && !this.#city && !this.#state && !this.#country && !this.#type_address)
        ) {
            return false;
        }
        return true;
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `Direccion {
            Street: ${this.#street},
            Number: ${this.#number},
            City: ${this.#city},
            State: ${this.#state},
            
            Country: ${this.#country},
            Type Address: ${this.#type_address},
            customer_id: ${this.#customer_id},
            longitud:${this.#longitud},
            latitud:${this.#latitud}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            street: this.#street,
            number: this.#number,
            city: this.#city,
            state: this.#state,
           
            country: this.#country,
            type_address: this.#type_address,
            customer_id: this.#customer_id,
            latitud:this.#latitud,
            longitud:this.#longitud
        };
    }
}

export default Direccion;
