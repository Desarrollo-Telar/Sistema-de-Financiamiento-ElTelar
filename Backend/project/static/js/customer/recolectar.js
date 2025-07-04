
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
    const form_data = new FormData();
    form_data.append('user_id', document.getElementById('user_id').value);
    form_data.append('immigration_status_id', document.getElementById('immigration_status_id').value);
    form_data.append('first_name', document.getElementById('first_name').value);
    form_data.append('last_name', document.getElementById('last_name').value);
    form_data.append('type_identification', document.getElementById('type_identification').value);
    form_data.append('identification_number', document.getElementById('identification_number').value);
    form_data.append('telephone', document.getElementById('telephone').value);
    form_data.append('email', document.getElementById('email').value);
    form_data.append('status', document.getElementById('status').value);
    form_data.append('date_birth', document.getElementById('date_birth').value);
    form_data.append('number_nit', document.getElementById('number_nit').value);
    form_data.append('place_birth', document.getElementById('place_birth').value);
    form_data.append('marital_status', document.getElementById('marital_status').value);
    form_data.append('profession_trade', document.getElementById('profession_trade').value);

    form_data.append('gender', document.getElementById('gender').value);
    form_data.append('nationality', document.getElementById('nationality').value || "GUATEMALTECA");
    form_data.append('person_type', document.getElementById('person_type').value);
    form_data.append('description', document.getElementById('description_customer').value);
    form_data.append('new_asesor_credito', document.getElementById('asesor').value ||  document.getElementById('user_id').value);
    form_data.append('fehca_vencimiento_de_tipo_identificacion', document.getElementById('fehca_vencimiento_de_tipo_identificacion').value);

    return form_data
}



// ------------------------------------------------
//                  DIRECCIONES
// ------------------------------------------------

import { get_departamento, get_municipio } from '../API/address/get_api.js'


let departamento1 = await get_departamento(document.getElementById('city1').value || 1);
let departamento2 = await get_departamento(document.getElementById('city2').value || 1);

let municipio1 = await get_municipio(document.getElementById('state1').value || 1);
let municipio2 = await get_municipio(document.getElementById('state2').value || 1);


export function recoletarInformacionDireccionPersonal(customer_id) {
    const form_data = new FormData();
    form_data.append('street', document.getElementById('street1').value);
    form_data.append('number', document.getElementById('number1').value);
    form_data.append('city', document.getElementById('city1').value);
    form_data.append('state', document.getElementById('state1').value);
    form_data.append('country', document.getElementById('country1').value);
    form_data.append('type_address', 'Dirección Personal');
    form_data.append('latitud', document.getElementById('latitud1').value);
    form_data.append('longitud', document.getElementById('longitud1').value);
    form_data.append('customer_id', customer_id);
    return form_data;

}

export function recoletarInformacionDireccionTrabajo(customer_id) {
    const form_data = new FormData();
    form_data.append('street', document.getElementById('street2').value);
    form_data.append('number', document.getElementById('number2').value);
    form_data.append('city', document.getElementById('city2').value);
    form_data.append('state', document.getElementById('state2').value);
    form_data.append('country', document.getElementById('country2').value);
    form_data.append('type_address', 'Dirección de Trabajo');
    form_data.append('latitud', document.getElementById('latitud2').value);
    form_data.append('longitud', document.getElementById('longitud2').value);
    form_data.append('customer_id', customer_id);
    return form_data;
}


// ------------------------------------------------
//                  INFORMACION LABORAL
// ------------------------------------------------

export function recolectarInformacionLaboral(customer_id) {
    const form_data = new FormData();
    let sourceOfIncome1 = document.getElementById('source_of_income1').value;

    if (sourceOfIncome1 === 'Otra') {
        form_data.append('source_of_income', document.getElementById('source_of_income2').value);
        form_data.append('nit', document.getElementById('nit').value);
        form_data.append('phone_number', document.getElementById('phone_number2').value);
        form_data.append('salary', document.getElementById('salary2').value);
        form_data.append('customer_id', customer_id);
    } else {
        form_data.append('position', document.getElementById('position').value);
        form_data.append('company_name', document.getElementById('company_name').value);
        form_data.append('start_date', document.getElementById('start_date').value);
        form_data.append('description', document.getElementById('description').value);
        form_data.append('salary', document.getElementById('salary').value);
        form_data.append('working_hours', document.getElementById('working_hours').value);
        form_data.append('phone_number', document.getElementById('phone_number1').value);
        form_data.append('source_of_income', document.getElementById('source_of_income1').value);
        form_data.append('income_detail', document.getElementById('income_detail').value);
        form_data.append('employment_status', document.getElementById('employment_status').value);
        form_data.append('customer_id', customer_id);
    }

    return form_data;
}




// ------------------------------------------------
//                  PLAN DE INVERSION
// ------------------------------------------------
export function recoletarInformacionPlanInversion(customer_id) {
    const form_data = new FormData();
    form_data.append('type_of_product_or_service', document.getElementById('type_of_product_or_service').value);
    form_data.append('total_value_of_the_product_or_service', document.getElementById('total_value_of_the_product_or_service').value);
    form_data.append('investment_plan_description', document.getElementById('investment_plan_description').value);
    form_data.append('initial_amount', document.getElementById('initial_amount').value);
    form_data.append('monthly_amount', document.getElementById('monthly_amount').value);
    form_data.append('transfers_or_transfer_of_funds', document.getElementById('transfers_or_transfer_of_funds').value);
    form_data.append('type_of_transfers_or_transfer_of_funds', document.getElementById('type_of_transfers_or_transfer_of_funds').value);
    form_data.append('customer_id', customer_id);
    return form_data;

}



// ------------------------------------------------
//                  REFERENCIAS
// ------------------------------------------------
export function recoletarInformacionReferencias(customer_id) {
    let referencias = [
        new Referencia(),
        new Referencia(),
        new Referencia(),
        new Referencia(),
    ];

    referencias[0].full_name = document.getElementById('full_name1').value;
    referencias[0].phone_number = document.getElementById('phone_number3').value;
    referencias[0].reference_type = 'Personales';
    referencias[0].customer_id = customer_id;

    referencias[1].full_name = document.getElementById('full_name2').value;
    referencias[1].phone_number = document.getElementById('phone_number4').value;
    referencias[1].reference_type = 'Personales';
    referencias[1].customer_id = customer_id;

    referencias[2].full_name = document.getElementById('full_name3').value;
    referencias[2].phone_number = document.getElementById('phone_number5').value;
    referencias[2].reference_type = document.getElementById('reference3').value;
    referencias[2].customer_id = customer_id;

    referencias[3].full_name = document.getElementById('full_name4').value;
    referencias[3].phone_number = document.getElementById('phone_number6').value;
    referencias[3].reference_type = document.getElementById('reference4').value;
    referencias[3].customer_id = customer_id;

    return referencias;

}
