import { urls } from '../API/urls_api.js';
import { postCustomer } from '../API/customer/post_api.js';
import { postDireccion } from '../API/address/post_api.js';
import { postPlanInversion } from '../API/investmentplan/post_api.js';


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
            let source_of_income = document.getElementById('source_of_income1').value;

            if (source_of_income === 'Otra'){

            }else{

            }

            // ------------- PLAN DE INVERSION -----------------
            postPlanInversion(urls.api_url_investment_plan, customer_id)
                .then(data => console.log('Plan de Inversion registrado con exito.', data))
                .catch(error => console.error('Error en el registro de plan de inversion', error))


        })
        .catch(error => console.error('Error al registrar el cliente:', error));



});