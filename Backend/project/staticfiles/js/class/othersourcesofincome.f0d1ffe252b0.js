export class OtraInformacionLaboral {
    #source_of_income;
    #nit;
    #phone_number;
    #customer_id;
    #salary;

    constructor(source_of_income='', nit='', phone_number='', customer_id = '',salary='') {
        this.#source_of_income = source_of_income;
        this.#nit = nit;
        this.#phone_number = phone_number;
        this.#customer_id = customer_id;
        this.#salary = salary;
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

    get salary() {
        return this.#salary;
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

    set salary(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el salario del cliente de su informacion laboral');
            throw new Error('Debe ingresar el salario del del cliente de su informacion laboral');
        }
        this.#salary = value.trim();
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

    // validar
    validar(){
        if(
            (
                this.#source_of_income.trim() ==='' &&
                this.#nit.trim() ===''&&
                this.#phone_number.trim() ==='' &&
               
                this.#salary.trim() ===''
            )||
            (
                !this.#source_of_income &&
                !this.#nit&&
                !this.#phone_number &&
               
                !this.#salary
            )
        ){
            return false;
        }
        return true;
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `OtraInformacionLaboral {
            Source of Income: ${this.#source_of_income},
            NIT: ${this.#nit},
            Phone Number: ${this.#phone_number},
            Salary: ${this.#salary},
            Cliente: ${this.#customer_id}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            source_of_income: this.#source_of_income,
            nit: this.#nit,
            phone_number: this.#phone_number,
            customer_id:this.#customer_id,
            salary:this.#salary
        };
    }
}

export default OtraInformacionLaboral;
