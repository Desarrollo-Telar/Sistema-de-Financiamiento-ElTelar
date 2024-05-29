import { urls } from '../API/urls_api.js';
import { postCustomer } from '../API/customer/post_api.js';
import { postDireccion } from '../API/address/post_api.js';
import { postPlanInversion } from '../API/investmentplan/post_api.js';
import { postLaboral } from '../API/workinginformation/post_api.js';
import { postReferencia } from '../API/reference/post_api.js';



document.getElementById('customer').addEventListener('submit', function (event) {
    event.preventDefault();
    let customer_id;
    
    
        postCustomer(urls.api_url_cliente)
            .then(data => {
                console.log('Cliente registrado con éxito:', data);
                customer_id = data.id;
    
                // Registra la dirección
                return postDireccion(urls.api_url_direccion, customer_id);
            })
            .then(data => {
                console.log('Dirección registrada con éxito:', data);
    
                // Registra la información laboral
                return postLaboral(customer_id);
            })
    
            .then(data => {
                console.log('Información laboral registrada con éxito:', data);
    
                // Registra el plan de inversión
                return postPlanInversion(urls.api_url_investment_plan, customer_id);
            })
    
            .then(data => {
                console.log('Plan de inversión registrado con éxito:', data);
    
                // Registra las referencias
                return postReferencia(urls.api_url_referencia, customer_id);
            })
            
            .then(data => {
                console.log('Referencias guardadas con éxito:', data);
                alert('¡Formulario enviado con éxito!');
            })
            .catch(error => {
                console.error('Error al registrar los datos:', error);
                alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
            });
    
    
});
