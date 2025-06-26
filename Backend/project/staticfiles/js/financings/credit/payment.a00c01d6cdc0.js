
import {urls, urls_p} from '../../API/urls_api.js'

document.getElementById('pago').addEventListener('submit', async function (event) {
    event.preventDefault();
    console.log('BUEEEENOOOO')
    const credit = document.getElementById('credit').value || 0;
    const cliente = document.getElementById('cliente').value || 0;
    let formData = new FormData();

    if (credit > 0){
        formData.append('credit', document.getElementById('credit').value);
    }
    if (cliente > 0){
        formData.append('cliente', document.getElementById('cliente').value);
    }
    if (cliente === 0 && credit ===0){
        Swal.fire({
            icon: "error",
            title: `Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.`,
            text:`No señalo para quien iba el registro de esta boleta`,
            timer: 3000,
            showConfirmButton: false,
        });
        throw new Error('No se puede enviar el formulario')
    }
        
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
            Swal.fire({
                icon: "success",
                title: `Registro Completado`,
                text: '¡Formulario enviado con éxito!',
                timer: 3000,
                showConfirmButton: false,
            });
            setTimeout(() => { window.history.back(); }, 1000);
        })
        .catch(error => {
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
        });
});