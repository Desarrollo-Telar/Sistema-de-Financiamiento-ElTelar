
import { urls_p, urls } from '../urls_api.js'

const URLO = urls_p.api_url_otra_informacion_laboral;
const URLW = urls_p.api_url_informacion_laboral;


export async function postLaboral(formData) {
    try {
        const sourceOfIncome1 = document.getElementById('source_of_income1').value;
        const urls = sourceOfIncome1 === 'Otra' ? URLO : URLW;

        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) {
            throw new Error('CSRF token not found');
        }
        const csrfToken = csrfTokenElement.getAttribute('content');

        const response = await axios({
            method: 'post',
            url: urls,
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrfToken
            },
            data: formData
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
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
        throw error; // Lanza el error para que pueda manejarse en un nivel superior
    }
}
