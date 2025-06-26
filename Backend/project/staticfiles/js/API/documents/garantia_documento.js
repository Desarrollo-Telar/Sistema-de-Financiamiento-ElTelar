import {urls_p} from '../urls_api.js'

const URL = urls_p.api_url_documento_garantia;

export async function registrar_documento_garantia(formData) {
    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    if (!csrfTokenElement) {
        throw new Error('CSRF token not found');
    }
    const csrfToken = csrfTokenElement.getAttribute('content');
    axios({
        method: 'post',
        url: URL,
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrfToken
        },
        data: formData
    })
        .then(response => {
            console.log(response.data);
            return response.data;
        })
        .catch(error => {
            if (error.response) {
                // El servidor respondió con un código de estado diferente a 2xx
                console.error('Error en la respuesta del servidor:', error.response.data);
                console.error('Código de estado:', error.response.status);
            } else if (error.request) {
                // La solicitud fue hecha pero no hubo respuesta
                console.error('Error en la solicitud (no hubo respuesta):', error.request);
            } else {
                // Algo más pasó al hacer la solicitud
                console.error('Error:', error.message);
            }
        });
}