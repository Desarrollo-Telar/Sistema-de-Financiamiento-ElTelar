class Cliente {
    #first_name;
    #last_name;
    #type_identification;
    #identification_number;
    #telephone;
    #email;
    #status;
    #date_birth;
    #number_nit;
    #place_birth;
    #marital_status;
    #profession_trade;
    #gender;
    #nationality;
    #person_type;


    constructor(first_name = '', last_name = '', type_identification = '', identification_number = '',
        telephone = '', email = '', status = '', date_birth = '', number_nit = '', place_birth = '',
        marital_status = '', profession_trade = '', gender = '', nationality = '', person_type = '') {
        this.#first_name = first_name;
        this.#last_name = last_name;
        this.#type_identification = type_identification;
        this.#identification_number = identification_number;
        this.#telephone = telephone;
        this.#email = email;
        this.#status = status;
        this.#date_birth = date_birth;
        this.#number_nit = number_nit;
        this.#place_birth = place_birth;
        this.#marital_status = marital_status;
        this.#profession_trade = profession_trade;
        this.#gender = gender;
        this.#nationality = nationality;
        this.#person_type = person_type;
    }

    // Getters and Setters for each property
    get first_name() {
        return this.#first_name;
    }

    set first_name(value) {
        this.#first_name = value;
    }

    get last_name() {
        return this.#last_name;
    }

    set last_name(value) {
        this.#last_name = value;
    }

    get type_identification() {
        return this.#type_identification;
    }

    set type_identification(value) {
        this.#type_identification = value;
    }

    get identification_number() {
        return this.#identification_number;
    }

    set identification_number(value) {
        this.#identification_number = value;
    }

    get telephone() {
        return this.#telephone;
    }

    set telephone(value) {
        // Expresión regular para exactamente 8 dígitos
        const regex = /^\d{8}$/;

        // Validar el formato del número de teléfono
        if (!regex.test(value)) {
            console.error('Numero de telefono no valido, no cumple con el estandar de un numero de telefono. Verificar!!!')
            return false;
        }
        this.#telephone = value;
    }

    get email() {
        return this.#email;
    }

    set email(value) {
        // Expresión regular básica para validar el formato del correo electrónico
        const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        // Lista de dominios conocidos
        const dominiosConocidos = ['gmail.com', 'yahoo.com', 'outlook.com'];  // Agrega más dominios según sea necesario
        // Validar el formato del correo electrónico
        if (!regex.test(value)) {
            console.error('Verifique bien si esta escribiendo el correo electronico...')
            return false;
        }
        // Obtener el dominio del correo electrónico
        const dominio = value.split('@')[1];

        // Verificar si el dominio está en la lista de dominios conocidos
        if (!dominiosConocidos.includes(dominio)) {
            console.error('Verifique bien si esta escribiendo el dominio del correo electronico...')
            return false;
        }
        this.#email = value;


    }

    get status() {
        return this.#status;
    }

    set status(value) {
        this.#status = value;
    }

    get date_birth() {
        return this.#date_birth;
    }

    set date_birth(value) {
        this.#date_birth = value;
    }

    get number_nit() {
        return this.#number_nit;
    }

    set number_nit(value) {
        this.#number_nit = value;
    }

    get place_birth() {
        return this.#place_birth;
    }

    set place_birth(value) {
        this.#place_birth = value;
    }

    get marital_status() {
        return this.#marital_status;
    }

    set marital_status(value) {
        this.#marital_status = value;
    }

    get profession_trade() {
        return this.#profession_trade;
    }

    set profession_trade(value) {
        this.#profession_trade = value;
    }

    get gender() {
        return this.#gender;
    }

    set gender(value) {
        this.#gender = value;
    }

    get nationality() {
        return this.#nationality;
    }

    set nationality(value) {
        this.#nationality = value;
    }

    get person_type() {
        return this.#person_type;
    }

    set person_type(value) {
        this.#person_type = value;
    }
    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            first_name: this.#first_name,
            last_name: this.#last_name,
            type_identification: this.#type_identification,
            identification_number: this.#identification_number,
            telephone: this.#telephone,
            email: this.#email,
            status: this.#status,
            date_birth: this.#date_birth,
            number_nit: this.#number_nit,
            place_birth: this.#place_birth,
            marital_status: this.#marital_status,
            profession_trade: this.#profession_trade,
            gender: this.#gender,
            nationality: this.#nationality,
            person_type: this.#person_type
        };
    }
    // Método toString para representar el objeto como una cadena
    toString() {
        return `Cliente {
            Nombre: ${this.#first_name}, 
            Apellido: ${this.#last_name},
            Tipo de Identificación: ${this.#type_identification},
            Número de Identificación: ${this.#identification_number},
            Teléfono: ${this.#telephone},
            Email: ${this.#email},
            Estado: ${this.#status},
            Fecha de Nacimiento: ${this.#date_birth},
            Número NIT: ${this.#number_nit},
            Lugar de Nacimiento: ${this.#place_birth},
            Estado Civil: ${this.#marital_status},
            Profesión/Oficio: ${this.#profession_trade},
            Género: ${this.#gender},
            Nacionalidad: ${this.#nationality},
            Tipo de Persona: ${this.#person_type}
        }`;
    }
}

export default Cliente;
