// Constructor de la clase



export class Cliente {
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
    #immigration_status_id;
    #user_id;


    constructor(first_name = '', last_name = '', type_identification = '', identification_number = '',
        telephone = '', email = '', status = '', date_birth = '', number_nit = '', place_birth = '',
        marital_status = '', profession_trade = '', gender = '', nationality = '', person_type = '', immigration_status_id='', user_id='') {
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
        this.#immigration_status_id = immigration_status_id;
        this.#user_id = user_id;
    }

    // Getters and Setters for each property
    get first_name() {
        return this.#first_name;
    }

    get last_name() {
        return this.#last_name;
    }

    get type_identification() {
        return this.#type_identification;
    }

    get identification_number() {
        return this.#identification_number;
    }

    get telephone() {
        return this.#telephone;
    }

    get email() {
        return this.#email;
    }

    get status() {
        return this.#status;
    }

    get date_birth() {
        return this.#date_birth;
    }

    get number_nit() {
        return this.#number_nit;
    }

    get place_birth() {
        return this.#place_birth;
    }

    get marital_status() {
        return this.#marital_status;
    }

    get profession_trade() {
        return this.#profession_trade;
    }

    get gender() {
        return this.#gender;
    }

    get nationality() {
        return this.#nationality;
    }

    get person_type() {
        return this.#person_type;
    }

    get immigration_status_id(){
        return this.#immigration_status_id;
    }

    get user_id(){
        return this.#user_id;
    }

    set first_name(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el nombre del cliente');
            throw new Error('Debe ingresar el nombre del cliente');
        }
        
        this.#first_name = value.trim();
    }
        
    set last_name(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el apellido del cliente');
            throw new Error('Debe ingresar el apellido del cliente');
        }
        
        this.#last_name = value.trim();
    }
    
    set type_identification(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el tipo de identificación del cliente');
            throw new Error('Debe ingresar el tipo de identificación del cliente');
        }
        
        
        this.#type_identification = value.trim();
    }

    set identification_number(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero del tipo de identificación del cliente');
            throw new Error('Debe ingresar el numero del tipo de identificación del cliente');
        }
        
        
        this.#identification_number = value.trim();
       
    }

    set telephone(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de telefono del cliente');
            throw new Error('Debe ingresar el numero de telefono del cliente');
        }
        
        
        // Expresión regular para exactamente 8 dígitos
        const regex = /^\d{8}$/;

        // Validar el formato del número de teléfono
        if (!regex.test(value)) {
            console.error('Numero de telefono no valido, no cumple con el estandar de un numero de telefono. Verificar!!!')
            alert('Número de teléfono no válido. Debe contener exactamente 8 dígitos.');
            throw new Error('Número de teléfono no válido. Debe contener exactamente 8 dígitos.');
            
        }
        this.#telephone = value.trim();
        
    }

    set email(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el correo electronico del cliente');
            throw new Error('Debe ingresar el correo electronico del cliente');
        }
        
        // Expresión regular básica para validar el formato del correo electrónico
        const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        // Lista de dominios conocidos
        const dominiosConocidos = ['gmail.com', 'yahoo.com', 'outlook.com'];  // Agrega más dominios según sea necesario
        // Validar el formato del correo electrónico
        if (!regex.test(value)) {
            console.error('Verifique bien si esta escribiendo el correo electronico...');
            //alert('Correo electrónico no válido. Verifique si está correctamente escrito.');
            throw new Error('Correo electrónico no válido. Verifique si está correctamente escrito.');
            
        }
        // Obtener el dominio del correo electrónico
        const dominio = value.split('@')[1];

        // Verificar si el dominio está en la lista de dominios conocidos
        if (!dominiosConocidos.includes(dominio)) {
            console.error('Verifique bien si esta escribiendo el dominio del correo electronico...');
            //alert('Correo electrónico no válido. Verifique si está correctamente escrito el dominio proporcionado.');
            throw new Error('Correo electrónico no válido. Verifique si está correctamente escrito el dominio proporcionado.');
            
        }
        this.#email = value.trim();


    }

    set status(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el status del cliente');
            throw new Error('Debe ingresar el correo electronico del cliente');
        }
        this.#status = value;
    }

    set date_birth(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la fecha de nacimiento del cliente');
            throw new Error('Debe ingresar el numero del tipo de identificación del cliente');
        }
        
        this.#date_birth = value.trim();
    }

    set number_nit(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de NIT cliente');
            throw new Error('Debe ingresar el numero de NIT cliente');
        }
        
        this.#number_nit = value.trim();
    }

    set place_birth(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el lugar de nacimiento del cliente');
            throw new Error('Debe ingresar el lugar de nacimiento del cliente');
        }
        this.#place_birth = value.trim();
    }

    set marital_status(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el estado civil del cliente');
            throw new Error('Debe ingresar el estado civil del cliente');
        }
        this.#marital_status = value.trim();
    }

    set profession_trade(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la profesion u oficio del cliente');
            throw new Error('Debe ingresar la profesion u oficio del cliente');
        }
        this.#profession_trade = value.trim();
    }

    set gender(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el genero del cliente');
            throw new Error('Debe ingresar el genero del cliente');
        }
        this.#gender = value.trim();
    }

    set nationality(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la nacionalidad del cliente');
            throw new Error('Debe ingresar la nacionalidad del cliente');
        }
        this.#nationality = value.trim();
    }

    set person_type(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el tipo de persona que es el cliente');
            throw new Error('Debe ingresar el tipo de persona que es el cliente');
        }
        this.#person_type = value.trim();
    }

    set immigration_status_id(value){
        if (!value || value.trim() === '') {
            alert('Debe ingresar la condicion migratoria del cliente');
            throw new Error('Debe ingresar la condicion migratoria del cliente');
        }
        
        this.#immigration_status_id = value.trim();
    }

    set user_id(value){
        if (!value || value.trim() === '') {
            alert('Debe ingresar el usuario que esta registrado a este cliente');
            throw new Error('Debe ingresar el usuario que esta registrado a este cliente');
        }
        
        
        this.#user_id = value.trim();
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
            person_type: this.#person_type,
            immigration_status_id: this.#immigration_status_id,
            user_id: this.#user_id,
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
            Tipo de Persona: ${this.#person_type},
            'Condicion Migratoria': ${this.#immigration_status_id},
            'Usuario': ${this.#user_id}
        }`;
    }
}

export default Cliente;
