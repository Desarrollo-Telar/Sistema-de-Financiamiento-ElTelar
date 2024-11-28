import { urls, urls_p } from '../API/urls_api.js';
import { postCustomer } from '../API/customer/post_api.js';
import { postDireccion } from '../API/address/post_api.js';
import { postPlanInversion } from '../API/investmentplan/post_api.js';
import { postLaboral } from '../API/workinginformation/post_api.js';
import { postReferencia } from '../API/reference/post_api.js';

import {alerta_m} from '../alertas/alertas.js'

import {
    recoletarInformacionCliente, 
    recoletarInformacionDirecciones,
    recolectarInformacionLaboral,
    recoletarInformacionPlanInversion,
    recoletarInformacionReferencias
} from '../customer/recolectar.js';



document.getElementById('customer').addEventListener('submit', async function (event) {
    event.preventDefault();
    let customer_id;

    try {
        let cliente = recoletarInformacionCliente();
        if(!cliente.validar()){
            
            alerta_m('Falta Informacion sobre el cliente',false);
            throw new Error('Falta Informacion sobre el cliente');

        }
        
        let direcciones = recoletarInformacionDirecciones();
        direcciones.forEach(element =>{
            if(!element.validar()){
                
                alerta_m('Falta Informacion las direcciones del cliente',false);
                throw new Error('Falta Informacion las direcciones del cliente');

            }
        })

        let laboral = recolectarInformacionLaboral();
        if(!laboral.validar()){
            
            alerta_m('Falta Informacion sobre información laboral del cliente',false);
            throw new Error('Falta Informacion sobre informacion laboral del cliente');
        }

        let destino = recoletarInformacionPlanInversion();
        if(!destino.validar()){
            
            alerta_m('Falta Informacion sobre informacion del destino del cliente',false);
            throw new Error('Falta Informacion sobre informacion del destino del cliente');
        }

        let referencias = recoletarInformacionReferencias();
        referencias.forEach(element =>{
            if(!element.validar()){
              
                alerta_m('Falta Informacion sobre referencias del cliente',false);
                throw new Error('Falta Informacion sobre las referencias del cliente');

            }
        })

        
        

        // Realizar llamadas a la API
        
        const customerData = await postCustomer(urls_p.api_url_cliente);
        console.log('Cliente registrado con éxito:', customerData);
        customer_id = customerData.id;
        

        const direccionData = await postDireccion(urls_p.api_url_direccion, customer_id);
        console.log('Dirección registrada con éxito:', direccionData);

        const laboralData = await postLaboral(customer_id);
        console.log('Información laboral registrada con éxito:', laboralData);

        const planInversionData = await postPlanInversion(urls_p.api_url_investment_plan, customer_id);
        console.log('Plan de inversión registrado con éxito:', planInversionData);

        const referenciaData = await postReferencia(urls_p.api_url_referencia, customer_id);
        console.log('Referencias guardadas con éxito:', referenciaData);

        alerta_m('Registro Realizado',true);

        // Redirigir a la página de éxito
        const { protocol, hostname, port } = window.location;
        const generar = `${protocol}//${hostname}:${port}/qr/${protocol}//${hostname}:${port}/formulario_ive/${customer_id}//`;
        console.log(generar);
        window.location.href = '/customers/';
        
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        if(customer_id){
            window.location.href = `/customers/delete/${customer_id}/`;

        }
        
        
        alerta_m(`Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo. ${error}`,false)
    }
});
