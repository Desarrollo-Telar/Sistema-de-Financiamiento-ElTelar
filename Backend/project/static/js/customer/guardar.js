import { urls } from '../API/urls_api.js';
import { postCustomer } from '../API/customer/post_api.js';
import { postDireccion } from '../API/address/post_api.js';
import { postPlanInversion } from '../API/investmentplan/post_api.js';
import { postLaboral } from '../API/workinginformation/post_api.js';
import { postReferencia } from '../API/reference/post_api.js';


import {recoletarInformacionCliente, recoletarInformacionDirecciones,recolectarInformacionLaboral,recoletarInformacionPlanInversion,recoletarInformacionReferencias} from '../customer/recolectar.js'

document.getElementById('customer').addEventListener('submit', async function (event) {
    event.preventDefault();
    let customer_id;

    try {
        
        
        recoletarInformacionCliente();
        const customerData = await postCustomer(urls.api_url_cliente);
        console.log('Cliente registrado con éxito:', customerData);
        customer_id = customerData.id;

        // Registra la dirección
    
        recoletarInformacionDirecciones(customer_id);
        const direccionData = await postDireccion(urls.api_url_direccion, customer_id);
        console.log('Dirección registrada con éxito:', direccionData);

        // Registra la información laboral
        recolectarInformacionLaboral(customer_id);
        const laboralData = await postLaboral(customer_id);
        console.log('Información laboral registrada con éxito:', laboralData);

        // Registra el plan de inversión
        
        recoletarInformacionPlanInversion(customer_id);
        const planInversionData = await postPlanInversion(urls.api_url_investment_plan, customer_id);
        console.log('Plan de inversión registrado con éxito:', planInversionData);

        // Registra las referencias
        recoletarInformacionReferencias(customer_id);
        const referenciaData = await postReferencia(urls.api_url_referencia, customer_id);
        console.log('Referencias guardadas con éxito:', referenciaData);

        alert('¡Formulario enviado con éxito!');
        // Redirigir a la página de éxito después de enviar todas las referencias
        let hostname = window.location.hostname;
        let protocol = window.location.protocol;
        let port = window.location.port;
        let fullUrl = window.location.href;
        //http://127.0.0.1:8000/qr/http://127.0.0.1:8000/formulario_ive/<int:id>//
        //formulario_ive/<int:id>/
        let generar = `${protocol}//${hostname}:${port}/qr/${protocol}//${hostname}:${port}/formulario_ive/${customer_id}//`;

        console.log(generar);
        //window.location.href = generar;
        window.location.href = '/customers/';
        
        
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        //window.location.href = '/customers/delete/'+customer_id+'/';
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }


});

