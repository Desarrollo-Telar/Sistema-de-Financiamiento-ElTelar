
import Cliente from '../class/customer.js';
import Direccion from '../class/address.js';
import PlanInversion from '../class/investmentplan.js';
import OtraInformacionLaboral from '../class/othersourcesofincome.js';
import Referencia from '../class/reference.js';
import InformacionLaboral from '../class/workinginformation.js';

// ------------------------------------------------
//                  CLIENTE
// ------------------------------------------------
export function recoletarInformacionCliente() {
    let cliente = new Cliente();
    cliente.first_name = document.getElementById('first_name').value;
    cliente.last_name = document.getElementById('last_name').value;
    cliente.email = document.getElementById('email').value;
    cliente.telephone = document.getElementById('telephone').value;
    cliente.type_identification = document.getElementById('type_identification').value;
    cliente.identification_number = document.getElementById('identification_number').value;
    cliente.date_birth = document.getElementById('date_birth').value;
    cliente.place_birth = document.getElementById('place_birth').value;
    cliente.nationality = document.getElementById('nationality').value;
    cliente.number_nit = document.getElementById('number_nit').value;
    cliente.gender = document.getElementById('gender').value;
    cliente.marital_status = document.getElementById('marital_status').value;
    cliente.profession_trade = document.getElementById('profession_trade').value;
    cliente.person_type = document.getElementById('person_type').value;
    cliente.status = document.getElementById('status').value;

}




// ------------------------------------------------
//                  DIRECCIONES
// ------------------------------------------------

export function recoletarInformacionDirecciones() {
    let direcciones = [
        new Direccion(),
        new Direccion(),
    ];

    direcciones[0].street = document.getElementById('street1').value;
    direcciones[0].number = document.getElementById('number1').value;
    direcciones[0].city = document.getElementById('city1').value;
    direcciones[0].state = document.getElementById('state1').value;
    direcciones[0].postal_code = document.getElementById('postal_code1').value;
    direcciones[0].country = document.getElementById('country1').value;
    direcciones[0].type_address = 'Dirección Personal';

    direcciones[1].street = document.getElementById('street2').value;
    direcciones[1].number = document.getElementById('number2').value;
    direcciones[1].city = document.getElementById('city2').value;
    direcciones[1].state = document.getElementById('state2').value;
    direcciones[1].postal_code = document.getElementById('postal_code2').value;
    direcciones[1].country = document.getElementById('country2').value;
    direcciones[1].type_address = 'Dirección de Trabajo';


}


// ------------------------------------------------
//                  INFORMACION LABORAL
// ------------------------------------------------

export function recoletarInformacionLaboral() {
    let informacionLaboral = new InformacionLaboral();
    informacionLaboral.source_of_income = document.getElementById('source_of_income1').value;

    if (informacionLaboral.source_of_income === 'Otra') {
        let otraInformacionLaboral = new OtraInformacionLaboral();
        otraInformacionLaboral.source_of_income = document.getElementById('source_of_income2').value;
        otraInformacionLaboral.nit = document.getElementById('nit').value;
        otraInformacionLaboral.phone_number = document.getElementById('phone_number2').value;

    } else {
        informacionLaboral.position = document.getElementById('position').value;
        informacionLaboral.company_name = document.getElementById('company_name').value;
        informacionLaboral.start_date = document.getElementById('start_date').value;
        informacionLaboral.description = document.getElementById('description').value;
        informacionLaboral.salary = document.getElementById('salary').value;
        informacionLaboral.working_hours = document.getElementById('working_hours').value;
        informacionLaboral.phone_number = document.getElementById('phone_number1').value;
        informacionLaboral.income_detail = document.getElementById('income_detail').value;
        informacionLaboral.employment_status = document.getElementById('employment_status').value;

    }

}



// ------------------------------------------------
//                  PLAN DE INVERSION
// ------------------------------------------------
export function recoletarInformacionPlanInversion() {
    let planInversion = new PlanInversion();
    planInversion.type_of_product_or_service = document.getElementById('type_of_product_or_service').value;
    planInversion.total_value_of_the_product_or_service = document.getElementById('total_value_of_the_product_or_service').value;
    planInversion.investment_plan_description = document.getElementById('investment_plan_description').value;
    planInversion.initial_amount = document.getElementById('initial_amount').value;
    planInversion.monthly_amount = document.getElementById('monthly_amount').value;
    planInversion.transfers_or_transfer_of_funds = document.getElementById('transfers_or_transfer_of_funds').value;
    planInversion.type_of_transfers_or_transfer_of_funds = document.getElementById('type_of_transfers_or_transfer_of_funds').value;

}



// ------------------------------------------------
//                  REFERENCIAS
// ------------------------------------------------
export function recoletarInformacionReferencias(){
    let referencias = [
        new Referencia(),
        new Referencia(),
        new Referencia(),
        new Referencia(),
    ];
    
    referencias[0].full_name = document.getElementById('full_name1').value;
    referencias[0].phone_number = document.getElementById('phone_number3').value;
    referencias[0].reference_type = document.getElementById('Personales').value;
    
    referencias[1].full_name = document.getElementById('full_name2').value;
    referencias[1].phone_number = document.getElementById('phone_number4').value;
    referencias[1].reference_type = document.getElementById('Personales').value;
    
    referencias[2].full_name = document.getElementById('full_name3').value;
    referencias[2].phone_number = document.getElementById('phone_number5').value;
    referencias[2].reference_type = document.getElementById('reference3').value;
    
    referencias[3].full_name = document.getElementById('full_name3').value;
    referencias[3].phone_number = document.getElementById('phone_number6').value;
    referencias[3].reference_type = document.getElementById('reference3').value;

}
