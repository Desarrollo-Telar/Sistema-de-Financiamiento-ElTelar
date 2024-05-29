import { urls } from '../API/urls_api.js';
import {postCustomer} from '../API/customer/post_api.js';
import {postDireccion} from '../API/address/post_api.js';

/// Uso de la función
document.getElementById('customer').addEventListener('submit', function (event) {
    // Evitar el envío predeterminado del formulario
    event.preventDefault();
   

    
    postCustomer(urls.api_url_cliente)
        .then(data => {

            console.log('Cliente registrado con éxito:', data);
            
// --------------- DIRECCIONES ---------------------------
            postDireccion(urls.api_url_direccion,data.id)
            .then(data => {
                console.log('Direccion registrado con exito...',data);
                alert('¡Formulario enviado con éxito!');
            })
            .catch(error => console.error('Error en el registro de la direccion',error));

            
        })
        .catch(error => console.error('Error al registrar el cliente:', error));
   


});