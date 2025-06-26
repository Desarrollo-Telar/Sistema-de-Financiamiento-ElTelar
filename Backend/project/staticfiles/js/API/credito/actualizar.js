import { urls_p } from '../urls_api.js';

const URL = urls_p.api_url_credit;

export async function actualizar_credito(id, formData) {
    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    if (!csrfTokenElement) {
        throw new Error('CSRF token not found');
    }
    const csrfToken = csrfTokenElement.getAttribute('content');

    try {
        // Validar parámetros
        if (!id || !formData) {
            throw new Error('ID o FormData no proporcionados.');
        }

        // Realizar solicitud PATCH
        const response = await axios({
            method: 'patch',
            url: `${URL}${id}/`,
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrfToken
            },
            data: formData
        });

        console.log('Crédito actualizado con éxito:', response.data);
        return response.data; // Retornar datos de la respuesta

    } catch (error) {
        if (error.response) {
            console.error('Error en la respuesta del servidor:', error.response.data);
            console.error('Código de estado:', error.response.status);
        } else if (error.request) {
            console.error('Error en la solicitud (no hubo respuesta):', error.request);
        } else {
            console.error('Error:', error.message);
        }
        throw error; // Re-lanzar el error para manejo externo si es necesario
    }
}
