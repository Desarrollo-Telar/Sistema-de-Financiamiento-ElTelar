
import  Cliente  from "../class/customer.js";

import { Direccion } from '../class/address.js';
import { PlanInversion } from '../class/investmentplan.js';
import { OtraInformacionLaboral } from '../class/othersourcesofincome.js';
import { Referencia } from '../class/reference.js';
import { InformacionLaboral } from '../class/workinginformation.js';

// Informacion del formulario
document.getElementById('customer').addEventListener('submit', function (event) {
    // Evitar el envío predeterminado del formulario
    event.preventDefault();
    let customer = Cliente();
    customer.first_name = document.getElementById('first_name').value;
    console.log(customer.toJSON());
    /*
        // Obtener los datos del formulario
        var nombre = document.getElementById('fist_name').value;
       
    
        // Realizar la validación (ejemplo sencillo)
        if (nombre === '') {
            alert('El nombre del cliente es obligatorio');
            return false;
        }
    
        */

    // Si la validación es exitosa, se puede proceder con el envío del formulario
    alert('¡Formulario enviado con éxito!');

    // Opcionalmente, puedes enviar el formulario programáticamente si es necesario
    // this.submit();
});
