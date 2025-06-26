import {urls, urls_p} from '../../API/urls_api.js'

import {alerta_m} from '../../alertas/alertas.js'

document.getElementById('municipio').addEventListener('submit', async function (event) {
    event.preventDefault();

    const nombre = document.getElementById('nombre').value.trim();
    const depart = document.getElementById('depart').value.trim();

    if (!nombre || !depart) {
        alerta_m('Por favor, completa todos los campos obligatorios.', false);
        return;
    }

    try {
        const municipio = await registrar_municipio();
        console.log(municipio);
        alerta_m('REGISTRO COMPLETADO', true);
        setTimeout(() => { window.history.back(); }, 1000);
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alerta_m(`Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo. ${error}`, false);
    }
});

async function registrar_municipio() {
    let formData = new FormData();
    formData.append('nombre', document.getElementById('nombre').value);
    formData.append('depart', document.getElementById('depart').value);

    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    if (!csrfTokenElement) {
        alerta_m('Token CSRF no encontrado. Por favor, recarga la página e inténtalo de nuevo.', false);
        throw new Error('CSRF token not found');
    }
    const csrfToken = csrfTokenElement.getAttribute('content');

    try {
        const response = await axios.post(urls_p.api_url_municipio, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrfToken
            }
        });

        if (response.status === 201) { // Código para creación exitosa
            return response.data;
        } else {
            throw new Error('Respuesta inesperada del servidor.');
        }
    } catch (error) {
        if (error.response) {
            console.error('Error en la respuesta del servidor:', error.response.data);
            console.error('Código de estado:', error.response.status);
        } else if (error.request) {
            console.error('Error en la solicitud (no hubo respuesta):', error.request);
        } else {
            console.error('Error:', error.message);
        }
        throw error;
    }
}
