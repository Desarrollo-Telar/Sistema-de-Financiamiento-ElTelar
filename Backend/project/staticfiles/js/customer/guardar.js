import { urls } from '../API/urls_api.js';
import { postCustomer } from '../API/customer/post_api.js';
import { postDireccion } from '../API/address/post_api.js';
import { postPlanInversion } from '../API/investmentplan/post_api.js';
import { postLaboral } from '../API/workinginformation/post_api.js';
import { postReferencia } from '../API/reference/post_api.js';

import {
    recoletarInformacionCliente, 
    recoletarInformacionDirecciones,
    recolectarInformacionLaboral,
    recoletarInformacionPlanInversion,
    recoletarInformacionReferencias
} from '../customer/recolectar.js';

document.getElementById('customer').addEventListener('submit', async function (event) {
    event.preventDefault();

    try {
        /*
        let direccionData = recoletarInformacionDirecciones(1);
        direccionData.forEach(element => console.log(element.toJSON()));
        
       
*/
        

        // Realizar llamadas a la API
        
        const customerData = await postCustomer(urls.api_url_cliente);
        console.log('Cliente registrado con éxito:', customerData);
        const customer_id = customerData.id;
        

        const direccionData = await postDireccion(urls.api_url_direccion, customer_id);
        console.log('Dirección registrada con éxito:', direccionData);

        const laboralData = await postLaboral(customer_id);
        console.log('Información laboral registrada con éxito:', laboralData);

        const planInversionData = await postPlanInversion(urls.api_url_investment_plan, customer_id);
        console.log('Plan de inversión registrado con éxito:', planInversionData);

        const referenciaData = await postReferencia(urls.api_url_referencia, customer_id);
        console.log('Referencias guardadas con éxito:', referenciaData);

        alert('¡Formulario enviado con éxito!');

        // Redirigir a la página de éxito
        const { protocol, hostname, port } = window.location;
        const generar = `${protocol}//${hostname}:${port}/qr/${protocol}//${hostname}:${port}/formulario_ive/${customer_id}//`;
        console.log(generar);
        window.location.href = '/customers/';
        
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }
});
