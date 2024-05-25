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
    
    constructor(position='', company_name='', start_date='', description='', salary='',
                working_hours='', phone_number='', source_of_income='', income_detail='', employment_status='') {
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

    // Setters
    set position(value) {
        this.#position = value;
    }

    set company_name(value) {
        this.#company_name = value;
    }

    set start_date(value) {
        this.#start_date = value;
    }

    set description(value) {
        this.#description = value;
    }

    set salary(value) {
        this.#salary = value;
    }

    set working_hours(value) {
        this.#working_hours = value;
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

    set source_of_income(value) {
        this.#source_of_income = value;
    }

    set income_detail(value) {
        this.#income_detail = value;
    }

    set employment_status(value) {
        this.#employment_status = value;
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
            Employment Status: ${this.#employment_status}
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
            employment_status: this.#employment_status
        };
    }
}

export default InformacionLaboral;
