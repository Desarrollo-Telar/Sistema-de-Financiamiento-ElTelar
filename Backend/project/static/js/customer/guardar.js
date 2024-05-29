import { urls } from '../API/urls_api.js';
import { postCustomer } from '../API/customer/post_api.js';
import { postDireccion } from '../API/address/post_api.js';
import { postPlanInversion } from '../API/investmentplan/post_api.js';
import { postLaboral } from '../API/workinginformation/post_api.js';
import { postReferencia } from '../API/reference/post_api.js';

/// Uso de la función
document.getElementById('customer').addEventListener('submit', function (event) {
    // Evitar el envío predeterminado del formulario
    event.preventDefault();



    postCustomer(urls.api_url_cliente)
        .then(data => {

            console.log('Cliente registrado con éxito:', data);

            // --------------- DIRECCIONES ---------------------------
            customer_id = data.id;
            postDireccion(urls.api_url_direccion, customer_id)
                .then(data => {
                    console.log('Direccion registrado con exito...', data);
                    alert('¡Formulario enviado con éxito!');
                })
                .catch(error => console.error('Error en el registro de la direccion', error));

            // ------------- INFORMACION LABORAL -------------------
            postLaboral(customer_id)
                .then(data => {
                    console.log('Informacion laboral registrado con exito', data)
                })
                .catch(error => console.error('Error en el registro laboral del cliente', error));


            // ------------- PLAN DE INVERSION -----------------
            postPlanInversion(urls.api_url_investment_plan, customer_id)
                .then(data => console.log('Plan de Inversion registrado con exito.', data))
                .catch(error => console.error('Error en el registro de plan de inversion', error));

            // ------- REFERENCIAS -----------
            postReferencia(urls.api_url_referencia, customer_id)
            .then(data => console.log('Refencias guardadas con exito', data))
            .catch(error => console.error('Error en el registro de referencias', error));


        })
        .catch(error => console.error('Error al registrar el cliente:', error));



});