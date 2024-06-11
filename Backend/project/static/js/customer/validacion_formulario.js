
import { Cliente } from '../class/customer.js'

let cl = new Cliente();
const inputField_email = document.getElementById('email');
const outputDiv_email = document.getElementById('output_email');
// Agregar un event listener para el evento input


// Funcion que verifica que si esta bien escrito el correo electronico
inputField_email.addEventListener('input', function (event) {
    try{
        const inputValue = event.target.value;
        cl.email = inputValue;
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


// Funcion que verifica que si esta bien escrito el numero de nit
inputField_nit.addEventListener('input', function (event) {
    try{
        const inputValue = event.target.value;
        cl.number_nit = inputValue;
        outputDiv_nit.style.color = 'green';
        outputDiv_nit.textContent = `Numero de NIT Valido: ${cl.telephone}`;

    }catch(e){
        outputDiv_nit.style.color = 'red';
        outputDiv_nit.textContent = `${e}`;
    }
});

const inputField_cui = document.getElementById('identification_number');
const outputDiv_cui = document.getElementById('output_identification_number');
// Agregar un event listener para el evento input


// Funcion que verifica que si esta bien escrito el numero de nit
inputField_cui.addEventListener('input', function (event) {
    try{
        const inputValue = event.target.value;
        cl.identification_number = inputValue;
        outputDiv_cui.style.color = 'green';
        outputDiv_cui.textContent = `Numero de NIT Valido: ${cl.telephone}`;

    }catch(e){
        outputDiv_cui.style.color = 'red';
        outputDiv_cui.textContent = `${e}`;
    }
});