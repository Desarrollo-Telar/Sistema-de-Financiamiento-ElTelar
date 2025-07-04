// Constructor de la clase

import { filtro, fetchCustomerList } from '../API/customer/list_api.js'

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
    #description;
    #asesor;
    #fehca_vencimiento_de_tipo_identificacion;


    constructor(first_name = '', last_name = '', type_identification = '', identification_number = '',
        telephone = '', email = '', status = '', date_birth = '', number_nit = '', place_birth = '',
        marital_status = '', profession_trade = '', gender = '', nationality = '', person_type = '', immigration_status_id = '', user_id = '', description = '', asesor='',fehca_vencimiento_de_tipo_identificacion='') {
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
        this.#description = description;
        this.#asesor = asesor;
        this.#fehca_vencimiento_de_tipo_identificacion = fehca_vencimiento_de_tipo_identificacion;
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

    get immigration_status_id() {
        return this.#immigration_status_id;
    }

    get user_id() {
        return this.#user_id;
    }

    get description() {
        return this.#description;
    }

    get asesor(){
        return this.#asesor;
    }

    get fehca_vencimiento_de_tipo_identificacion(){
        return this.#fehca_vencimiento_de_tipo_identificacion;
    }

    set asesor(value){
        this.#asesor = value.trim();
    }
    set fehca_vencimiento_de_tipo_identificacion(value){
        this.#fehca_vencimiento_de_tipo_identificacion = value.trim();
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

    static async validateIDENTIFICATIONNUMBER(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero del tipo de identificación del cliente');
            throw new Error('Debe ingresar el numero del tipo de identificación del cliente');
        }
        // Expresión regular para exactamente 13 dígitos
        const regex = /^\d{20}$/;

        // Validar el formato del número de identificacion
        if (!regex.test(value)) {
            console.error('Numero de identificacion no valido. Verificar!!!')
            //alert('Numero de identificacion no valido. Verificar!!!');
            throw new Error('Numero de identificacion no valido. Verificar!!!');

        }
        // Verificar si el número de identificacion ya está registrado
        const customers = await fetchCustomerList();
        const encontrado = customers.some(cliente => cliente['identification_number'] === value);
        if (encontrado) {
            throw new Error('Número de identificacion no válido. Este número de identificacion ya ha sido registrado');
        }
        return value.trim();
    }

    async setIDENTIFICATIONNUMBER(value) {
        this.#identification_number = await Cliente.validateIDENTIFICATIONNUMBER(value);
    }

    set identification_number(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero del tipo de identificación del cliente');
            throw new Error('Debe ingresar el numero del tipo de identificación del cliente');
        }
        /*
        // Expresión regular para exactamente 13 dígitos
        const regex = /^\d{20}$/;

        // Validar el formato del número de identificacion
        if (!regex.test(value)) {
            console.error('Numero de identificacion no valido. Verificar!!!')
            //alert('Numero de identificacion no valido. Verificar!!!');
            throw new Error('Numero de identificacion no valido. Verificar!!!');

        }

        */
        this.#identification_number = value.trim();

    }

    set telephone(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de telefono del cliente');
            throw new Error('Debe ingresar el numero de telefono del cliente');
        }


        // Expresión regular para exactamente 8 dígitos
        const regex = /^\d{12}$/;
/*
        // Validar el formato del número de teléfono
        if (!regex.test(value)) {
            console.error('Numero de telefono no valido, no cumple con el estandar de un numero de telefono. Verificar!!!')
            //alert('Número de teléfono no válido. Debe contener exactamente 8 dígitos.');
            throw new Error('Número de teléfono no válido. Debe contener exactamente 8 dígitos.');

        }
        */
        this.#telephone = value.trim();

    }

    static async validateEMAIL(value) {
        if (!value || value.trim() === '') {
            //alert('Debe ingresar el correo electronico del cliente');
            throw new Error('Debe ingresar el correo electronico del cliente');
        }
        // Expresión regular básica para validar el formato del correo electrónico
        const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        // Lista de dominios conocidos
        const dominiosConocidos = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'];  // Agrega más dominios según sea necesario
        // Validar el formato del correo electrónico
        if (!regex.test(value)) {
            console.error('Verifique bien si esta escribiendo el correo electronico...');
            alert('Correo electrónico no válido. Verifique si está correctamente escrito.');
            throw new Error('Correo electrónico no válido. Verifique si está correctamente escrito.');

        }
        // Obtener el dominio del correo electrónico
        const dominio = value.split('@')[1];

        // Verificar si el dominio está en la lista de dominios conocidos
        if (!dominiosConocidos.includes(dominio)) {
            console.error('Verifique bien si esta escribiendo el dominio del correo electronico...');
            alert('Correo electrónico no válido. Verifique si está correctamente escrito el dominio proporcionado.');
            throw new Error('Correo electrónico no válido. Verifique si está correctamente escrito el dominio proporcionado.');

        }
        // Verificar si el número de EMAIL ya está registrado
        const customers = await fetchCustomerList();
        const encontrado = customers.some(cliente => cliente['email'] === value);
        if (encontrado) {
            throw new Error('Correo Electronico no válido. Este correo ya ha sido registrado');
        }

        return value.trim();

    }

    async setEMAIL(value) {
        this.#email = await Cliente.validateEMAIL(value);
    }

    set email(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el correo electronico del cliente');
            throw new Error('Debe ingresar el correo electronico del cliente');
        }
/*
        // Expresión regular básica para validar el formato del correo electrónico
        const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        // Lista de dominios conocidos
        const dominiosConocidos = ['gmail.com', 'yahoo.com', 'outlook.com'];  // Agrega más dominios según sea necesario
        // Validar el formato del correo electrónico
        if (!regex.test(value)) {
            console.error('Verifique bien si esta escribiendo el correo electronico...');
            alert('Correo electrónico no válido. Verifique si está correctamente escrito.');
            throw new Error('Correo electrónico no válido. Verifique si está correctamente escrito.');

        }
        // Obtener el dominio del correo electrónico
        const dominio = value.split('@')[1];

        // Verificar si el dominio está en la lista de dominios conocidos
        if (!dominiosConocidos.includes(dominio)) {
            console.error('Verifique bien si esta escribiendo el dominio del correo electronico...');
            alert('Correo electrónico no válido. Verifique si está correctamente escrito el dominio proporcionado.');
            throw new Error('Correo electrónico no válido. Verifique si está correctamente escrito el dominio proporcionado.');

        }
*/
        // Falta por agregar el filtro de ver si ya existe el correo electronico registrado
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

    static async validateNIT(value) {
        if (!value || value.trim() === '') {
            throw new Error('Debe ingresar el número de NIT del cliente');
        }
        /*

        const regex = /^(\d{7}-[A-Z]|\d{8}|\d{7}[A-Z]|\d{7}-\d{1})$/;

        // Validar el formato del número de NIT
        if (!regex.test(value)) {
            throw new Error('Número de NIT no válido. Verificar');
        }
*/
        // Verificar si el número de NIT ya está registrado
        const customers = await fetchCustomerList();
        const encontrado = customers.some(cliente => cliente['number_nit'] === value);
        if (encontrado) {
            throw new Error('Número de NIT no válido. Este número de NIT ya ha sido registrado');
        }

        return value.trim();
    }

    async setNumberNIT(value) {
        this.#number_nit = await Cliente.validateNIT(value);
    }

    set number_nit(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de NIT cliente');
            throw new Error('Debe ingresar el numero de NIT cliente');
        }
        /*
        const regex = /^(\d{7}-[A-Z]|\d{8}|\d{7}[A-Z]|\d{7}-\d{1})$/;

        // Validar el formato del número de nit
        if (!regex.test(value)) {
            console.error('Numero de NIT no valido. Verificar!!!')
            //alert('Numero de NIT no valido. Verificar!!!');
            throw new Error('Numero de NIT no valido. Verificar!!!');

        }
        */

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

    set immigration_status_id(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la condicion migratoria del cliente');
            throw new Error('Debe ingresar la condicion migratoria del cliente');
        }

        this.#immigration_status_id = value.trim();
    }

    set user_id(value) {
        this.#user_id = value;
    }

    set description(value) {
        this.#description = value;
    }

    // Validar que todos los campos no esten vacios
    validar() {
        
        if (
            (
                this.#first_name.trim() ==='' && this.#last_name.trim() ==='' && this.#type_identification.trim() ==='' && this.#identification_number.trim() ==='' && this.#telephone.trim() ==='' &&this.#email.trim() ==='' &&this.#status.trim() ==='' &&
                this.#date_birth.trim() ==='' &&this.#number_nit.trim() ==='' && this.#place_birth.trim() ==='' &&this.#marital_status.trim() ==='' &&this.#profession_trade.trim() ==='' &&this.#gender.trim() ==='' &&this.#nationality.trim() ==='' &&
                this.#person_type.trim() ==='' &&this.#immigration_status_id.trim() ==='' && this.#user_id.trim() ==='') ||
            (
                !this.#first_name && !this.#last_name && !this.#type_identification && !this.#identification_number && !this.#telephone &&!this.#email &&!this.#status &&!this.#date_birth &&!this.#number_nit &&
                !this.#place_birth &&!this.#marital_status &&!this.#profession_trade &&!this.#gender &&!this.#nationality &&!this.#person_type &&!this.#immigration_status_id && !this.#user_id )
        ) {
            return false;
        }
        return true;
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
            description: this.#description,
            fehca_vencimiento_de_tipo_identificacion:this.#fehca_vencimiento_de_tipo_identificacion,
            asesor:this.#asesor
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
            'Usuario': ${this.#user_id},
            'Descripcion': ${this.#description}
        }`;
    }
}

export default Cliente;
