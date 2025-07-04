
import {urls, urls_p} from '../../API/urls_api.js'

document.getElementById('pago').addEventListener('submit', async function (event) {
    event.preventDefault();
    console.log('BUEEEENOOOO')
    let formData = new FormData();
    formData.append('credit', document.getElementById('credit').value);
    formData.append('monto', document.getElementById('monto').value);
    formData.append('numero_referencia', document.getElementById('numero_referencia').value);
    formData.append('fecha_emision', document.getElementById('fecha_emision').value);
    formData.append('descripcion', document.getElementById('descripcion').value);
    formData.append('boleta', document.getElementById('boleta').files[0]); // El archivo
    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    if (!csrfTokenElement) {
        throw new Error('CSRF token not found');
    }
    const csrfToken = csrfTokenElement.getAttribute('content');

    axios({
        method: 'post',
        url: urls_p.api_url_pago,
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': csrfToken
        },
        data: formData
    })
        .then(response => {
            console.log(response.data);
            alert('¡Formulario enviado con éxito!');
            window.location.href = `/financings/payment/`;
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
});