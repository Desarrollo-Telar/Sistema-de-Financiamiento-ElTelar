
import { Cliente } from '../class/customer.js'

//output_name_customer
const first_name = document.getElementById('first_name');
const last_name = document.getElementById('last_name');



function updateOutput() {
    const output_name_customer = document.getElementById('output_name_customer');
    const workingInformation = document.getElementById('output_info_name_customer');
    const plan = document.getElementById('output_plan_name_customer');
    const refe = document.getElementById('output_refe_name_customer');
    const image = document.getElementById('output_image_name_customer');
    output_name_customer.textContent = `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    workingInformation.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    plan.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    refe.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    image.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
}

first_name.addEventListener('input', updateOutput);
last_name.addEventListener('input', updateOutput);

/*
const inputField_email = document.getElementById('email');
const outputDiv_email = document.getElementById('output_email');
// Agregar un event listener para el evento input



// Funcion que verifica que si esta bien escrito el correo electronico

inputField_email.addEventListener('input', async function (event) {
    let cl = new Cliente();
    try{
        await cl.setEMAIL(event.target.value);
        outputDiv_email.style.color = 'green';
        outputDiv_email.textContent = `Correo Electronico Valido: ${cl.email}`;

    }catch(e){
        outputDiv_email.style.color = 'red';
        outputDiv_email.textContent = `${e}`;
       


    }
 
});

const inputField_telefono = document.getElementById('telephone');
const outputDiv_telefono = document.getElementById('output_telephone');
// Agregar un event listener para el evento input


// Funcion que verifica que si esta bien escrito el numero de telefono

inputField_telefono.addEventListener('input', function (event) {
    let cl = new Cliente();
    try{
        const inputValue = event.target.value;
        cl.telephone = inputValue;
        outputDiv_telefono.style.color = 'green';
        outputDiv_telefono.textContent = `Numero de telefono Valido: ${cl.telephone}`;

    }catch(e){
        outputDiv_telefono.style.color = 'red';
        outputDiv_telefono.textContent = `${e}`;

    }

});

const inputField_nit = document.getElementById('number_nit');
const outputDiv_nit = document.getElementById('output_number_nit');

// Agregar un event listener para el evento input
inputField_nit.addEventListener('input', async function (event) {
    let cl = new Cliente();
    try {
        await cl.setNumberNIT(event.target.value);
        outputDiv_nit.style.color = 'green';
        outputDiv_nit.textContent = 'Numero de nit valido: ' + cl.number_nit;
    } catch (e) {
        outputDiv_nit.style.color = 'red';
        outputDiv_nit.textContent = `ERROR: ${e.message}`;
    }
});


const inputField_cui = document.getElementById('identification_number');
const outputDiv_cui = document.getElementById('output_identification_number');
// Agregar un event listener para el evento input


// Funcion que verifica que si esta bien escrito el numero de nit

inputField_cui.addEventListener('input', async function (event) {
    let cl = new Cliente();
    try{
        await cl.setIDENTIFICATIONNUMBER( event.target.value);
        outputDiv_cui.style.color = 'green';
        outputDiv_cui.textContent = `Numero de identificación Valido: ${cl.identification_number}`;

    }catch(e){
        outputDiv_cui.style.color = 'red';
        outputDiv_cui.textContent = `${e}`;        

    }

});
*/