
import { Cliente } from '../class/customer.js'

let cl = new Cliente();
const inputField_email = document.getElementById('email');
const outputDiv_email = document.getElementById('output_first_name');
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