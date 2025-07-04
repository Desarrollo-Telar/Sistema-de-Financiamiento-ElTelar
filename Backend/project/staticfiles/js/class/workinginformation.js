export class InformacionLaboral {
    #position;
    #company_name;
    #start_date;
    #description;
    #salary;
    #working_hours;
    #phone_number;
    #source_of_income;
    #income_detail;
    #employment_status;
    #customer_id;

    constructor(position = '', company_name = '', start_date = '', description = '', salary = '',
        working_hours = '', phone_number = '', source_of_income = '', income_detail = '', employment_status = '', customer_id = '') {
        this.#position = position;
        this.#company_name = company_name;
        this.#start_date = start_date;
        this.#description = description;
        this.#salary = salary;
        this.#working_hours = working_hours;
        this.#phone_number = phone_number;
        this.#source_of_income = source_of_income;
        this.#income_detail = income_detail;
        this.#employment_status = employment_status;
        this.#customer_id = customer_id;
    }

    // Getters
    get position() {
        return this.#position;
    }

    get company_name() {
        return this.#company_name;
    }

    get start_date() {
        return this.#start_date;
    }

    get description() {
        return this.#description;
    }

    get salary() {
        return this.#salary;
    }

    get working_hours() {
        return this.#working_hours;
    }

    get phone_number() {
        return this.#phone_number;
    }

    get source_of_income() {
        return this.#source_of_income;
    }

    get income_detail() {
        return this.#income_detail;
    }

    get employment_status() {
        return this.#employment_status;
    }

    get customer_id() {
        return this.#customer_id;
    }

    // Setters
    set position(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la posicion del cliente de su informacion laboral');
            throw new Error('Debe ingresar la posicion del cliente de su informacion laboral');
        }


        this.#position = value.trim();
    }

    set company_name(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el nombre de la empresa del cliente de su informacion laboral');
            throw new Error('Debe ingresar el nombre de la empresa del cliente de su informacion laboral');
        }


        this.#company_name = value.trim();
    }

    set start_date(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar la fecha de inicio del cliente de su informacion laboral');
            throw new Error('Debe ingresar la fecha de inicio del cliente de su informacion laboral');
        }


        this.#start_date = value.trim();

    }

    set description(value) {
        this.#description = value;
    }

    set salary(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el salario del cliente de su informacion laboral');
            throw new Error('Debe ingresar el salario del del cliente de su informacion laboral');
        }
        this.#salary = value.trim();
    }

    set working_hours(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar las horario de trabajo del cliente de su informacion laboral');
            throw new Error('Debe ingresar las horario de trabajo del del cliente de su informacion laboral');
        }
        this.#working_hours = value.trim();
    }

    set phone_number(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el numero de telefono de trabajo del cliente de su informacion laboral');
            throw new Error('Debe ingresar el numero de telefono de trabajo del cliente de su informacion laboral');
        }
        // Expresión regular para exactamente 8 dígitos
        const regex = /^\d{8}$/;

        // Validar el formato del número de teléfono
        if (!regex.test(value)) {
            console.error('Numero de telefono no valido, no cumple con el estandar de un numero de telefono. Verificar!!!')
            throw new Error('Número de teléfono no válido. Debe contener exactamente 8 dígitos.');
        }

        this.#phone_number = value;
    }

    set source_of_income(value) {
        this.#source_of_income = value;
    }

    set income_detail(value) {
        this.#income_detail = value;
    }

    set employment_status(value) {
        this.#employment_status = value;
    }

    set customer_id(value) {
        this.#customer_id = value;
    }

    validar() {
        if (
            (
                this.#position.trim() === '' &&
                this.#company_name.trim() === '' &&
                this.#start_date.trim() === '' &&
              //  this.#description.trim() === '' &&
                this.#salary.trim() === '' &&
                this.#working_hours.trim() === '' &&
                this.#phone_number.trim() === '' &&
                this.#employment_status.trim() === '' 
                ) ||
            (
                !this.#position &&
                !this.#company_name &&
                !this.#start_date &&
                //!this.#description &&
                !this.#salary &&
                !this.#working_hours &&
                !this.#phone_number &&
                !this.#employment_status 
            )
        ) {
            return false;
        }
        return true;
    }


    // Método toString para representar el objeto como una cadena
    toString() {
        return `InformacionLaboral {
            Position: ${this.#position},
            Company Name: ${this.#company_name},
            Start Date: ${this.#start_date},
            Description: ${this.#description},
            Salary: ${this.#salary},
            Working Hours: ${this.#working_hours},
            Phone Number: ${this.#phone_number},
            Source of Income: ${this.#source_of_income},
            Income Detail: ${this.#income_detail},
            Employment Status: ${this.#employment_status},
            'Cliente: ${this.#customer_id}
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            position: this.#position,
            company_name: this.#company_name,
            start_date: this.#start_date,
            description: this.#description,
            salary: this.#salary,
            working_hours: this.#working_hours,
            phone_number: this.#phone_number,
            source_of_income: this.#source_of_income,
            income_detail: this.#income_detail,
            employment_status: this.#employment_status,
            customer_id: this.#customer_id
        };
    }
}

export default InformacionLaboral;
