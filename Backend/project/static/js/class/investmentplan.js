export class PlanInversion {
    #type_of_product_or_service;
    #total_value_of_the_product_or_service;
    #investment_plan_description;
    #initial_amount;
    #monthly_amount;
    #transfers_or_transfer_of_funds;
    #type_of_transfers_or_transfer_of_funds;
    #customer_id;

    constructor(type_of_product_or_service='', total_value_of_the_product_or_service='', investment_plan_description='', initial_amount='', 
    monthly_amount='', transfers_or_transfer_of_funds='', type_of_transfers_or_transfer_of_funds='', customer_id='') {
        this.#type_of_product_or_service = type_of_product_or_service;
        this.#total_value_of_the_product_or_service = total_value_of_the_product_or_service;
        this.#investment_plan_description = investment_plan_description;
        this.#initial_amount = initial_amount;
        this.#monthly_amount = monthly_amount;
        this.#transfers_or_transfer_of_funds = transfers_or_transfer_of_funds;
        this.#type_of_transfers_or_transfer_of_funds = type_of_transfers_or_transfer_of_funds;
        this.#customer_id = customer_id;
    }

    // Getters
    get type_of_product_or_service() {
        return this.#type_of_product_or_service;
    }

    get total_value_of_the_product_or_service() {
        return this.#total_value_of_the_product_or_service;
    }

    get investment_plan_description() {
        return this.#investment_plan_description;
    }

    get initial_amount() {
        return this.#initial_amount;
    }

    get monthly_amount() {
        return this.#monthly_amount;
    }

    get transfers_or_transfer_of_funds() {
        return this.#transfers_or_transfer_of_funds;
    }

    get type_of_transfers_or_transfer_of_funds() {
        return this.#type_of_transfers_or_transfer_of_funds;
    }

    get customer_id(){
        return this.#customer_id;
    }

    // Setters
    set type_of_product_or_service(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el Tipo Producto o Servicio del cliente');
            throw new Error('Debe ingresar el Tipo Producto o Servicio del cliente');
        }

        this.#type_of_product_or_service = value.trim();
    }

    set total_value_of_the_product_or_service(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el Valor total del producto o servicio del cliente');
            throw new Error('Debe ingresar el Valor total del producto o servicio del cliente');
        }

        this.#total_value_of_the_product_or_service = value.trim();
    }

    set investment_plan_description(value) {        

        this.#investment_plan_description = value.trim();
    }

    set initial_amount(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el Monto Inicial a manejar en el producto o servicios del cliente');
            throw new Error('Debe ingresar el Monto Inicial a manejar en el producto o servicios del cliente');
        }

        this.#initial_amount = value.trim();
    }

    set monthly_amount(value) {
        if (!value || value.trim() === '') {
            alert('Debe ingresar el Monto Inicial a manejar en el producto o servicios del cliente');
            throw new Error('Debe ingresar el Monto Inicial a manejar en el producto o servicios del cliente');
        }

        this.#monthly_amount = value.trim();
    }

    set transfers_or_transfer_of_funds(value) {
        this.#transfers_or_transfer_of_funds = value;
    }

    set type_of_transfers_or_transfer_of_funds(value) {
        this.#type_of_transfers_or_transfer_of_funds = value;
    }

    set customer_id(value){
        this.#customer_id = value;
    }

    // Validar
    validar(){
        if (
            (
                this.#type_of_product_or_service.trim() === '' &&
                this.#total_value_of_the_product_or_service.trim() === '' &&
                this.#initial_amount.trim() === '' &&
                this.#monthly_amount.trim() === '' 
            )||
            (
                !this.#type_of_product_or_service &&
                !this.#total_value_of_the_product_or_service &&
                !this.#initial_amount &&
                !this.#monthly_amount 
            )
        ){
            return false;
        }
        return true;
    }

    // Método toString para representar el objeto como una cadena
    toString() {
        return `PlanInversion {
            Type of Product or Service: ${this.#type_of_product_or_service},
            Total Value of the Product or Service: ${this.#total_value_of_the_product_or_service},
            Investment Plan Description: ${this.#investment_plan_description},
            Initial Amount: ${this.#initial_amount},
            Monthly Amount: ${this.#monthly_amount},
            Transfers or Transfer of Funds: ${this.#transfers_or_transfer_of_funds},
            Type of Transfers or Transfer of Funds: ${this.#type_of_transfers_or_transfer_of_funds},
            Cliente: ${this.#customer_id},
        }`;
    }

    // Método toJSON para convertir el objeto en una representación JSON
    toJSON() {
        return {
            type_of_product_or_service: this.#type_of_product_or_service,
            total_value_of_the_product_or_service: this.#total_value_of_the_product_or_service,
            investment_plan_description: this.#investment_plan_description,
            initial_amount: this.#initial_amount,
            monthly_amount: this.#monthly_amount,
            transfers_or_transfer_of_funds: this.#transfers_or_transfer_of_funds,
            type_of_transfers_or_transfer_of_funds: this.#type_of_transfers_or_transfer_of_funds,
            customer_id: this.#customer_id
        };
    }
}

export default PlanInversion;