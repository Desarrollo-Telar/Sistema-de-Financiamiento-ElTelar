import { urls, urls_p } from '../API/urls_api.js';
import { postCustomer } from '../API/customer/post_api.js';
import { postDireccion } from '../API/address/post_api.js';
import { postPlanInversion } from '../API/investmentplan/post_api.js';
import { postLaboral } from '../API/workinginformation/post_api.js';
import { postReferencia } from '../API/reference/post_api.js';

import { alerta_m } from '../alertas/alertas.js'

import {
    recoletarInformacionCliente,
    recoletarInformacionDireccionPersonal,
    recoletarInformacionDireccionTrabajo,
    recolectarInformacionLaboral,
    recoletarInformacionPlanInversion,
    recoletarInformacionReferencias
} from '../customer/recolectar.js';

import { validateFormFields } from '../customer/validacion_formulario.js'

document.getElementById('customer').addEventListener('submit', async function (event) {


    event.preventDefault(); // Evita el envío del formulario si hay campos vacíos.
    // Evita el envío del formulario si hay campos vacíos.
    let customer_id;

    try {

        // Realizar llamadas a la API
        const customerData = await postCustomer(recoletarInformacionCliente());
        console.log('Cliente registrado con éxito:', customerData);
        customer_id = customerData.id;

        let direcion_personal = recoletarInformacionDireccionPersonal(customer_id);
        let direcion_trabajo = recoletarInformacionDireccionTrabajo(customer_id);

        const direccionDataPersonal = await postDireccion(direcion_personal);
        console.log('Dirección Personal registrada con éxito:', direccionDataPersonal);

        let laboral = recolectarInformacionLaboral(customer_id);
        const laboralData = await postLaboral(laboral);
        console.log('Información laboral registrada con éxito:', laboralData);

        const direccionDataTrabajo = await postDireccion(direcion_trabajo);
        console.log('Dirección de la Fuente de Ingreso registrada con éxito:', direccionDataTrabajo);

        let destino = recoletarInformacionPlanInversion(customer_id);

        const planInversionData = await postPlanInversion(destino);
        console.log('Plan de inversión registrado con éxito:', planInversionData);

        const referenciaData = await postReferencia(urls_p.api_url_referencia, customer_id);
        console.log('Referencias guardadas con éxito:', referenciaData);

        alerta_m('Registro Realizado', true);

        // Redirigir a la página de éxito
        const { protocol, hostname, port } = window.location;
        const generar = `${protocol}//${hostname}:${port}/qr/${protocol}//${hostname}:${port}/formulario_ive/${customer_id}//`;
        console.log(generar);
        
        setTimeout(() => { window.location.href = '/customers/'; }, 1000);

    } catch (error) {
        console.error('Error al registrar los datos:', error);
        if (error.response) {
            console.error('Error en la respuesta del servidor:', error.response.data);
            Swal.fire({
                icon: "error",
                title: `Error ${error.response.status}`,
                text: error.response.data.message || 'Ocurrió un problema en el servidor.',
                timer: 3000,
                showConfirmButton: false,
            });
        } else if (error.request) {
            console.error('Error en la solicitud:', error.request);
            Swal.fire({
                icon: "error",
                title: `Sin respuesta del servidor`,
                text: `No se obtuvo respuesta del servidor. Por favor, inténtalo más tarde.`,
                timer: 3000,
                showConfirmButton: false,
            });
        } else {
            console.error('Error:', error.message);
            Swal.fire({
                icon: "error",
                title: `Error inesperado`,
                text: error.message,
                timer: 3000,
                showConfirmButton: false,
            });
        }
        if (customer_id) {
            setTimeout(() => { window.location.href = `/customers/delete/${customer_id}/`; }, 1000);

        }
        
        
    }


});
