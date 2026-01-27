
import {urls, urls_p} from '../../API/urls_api.js'

import {ocultar, mostrar} from '../funciones_externas/ocultar_mostrar.js'
document.getElementById('pago').addEventListener('submit', async function (event) {
    event.preventDefault();

    ocultar(document.getElementById('pago'));
    
    console.log('Iniciando envío de formulario');

    const creditInput = document.getElementById('credit');
    const clienteInput = document.getElementById('cliente');

    const credit = creditInput ? parseInt(creditInput.value) : 0;
    const cliente = clienteInput ? parseInt(clienteInput.value) : 0;

    // Validación básica
    if (cliente === 0 && credit === 0) {
        Swal.fire({
            icon: "error",
            title: `Hubo un error al enviar el formulario.`,
            text: `No se indicó para quién es esta boleta.`,
            timer: 3000,
            showConfirmButton: false,
        });
        mostrar(document.getElementById('pago'));
        return;
    }

    let formData = new FormData();

    // Solo agregar si existen y son válidos
    if (!isNaN(credit) && credit > 0) {
        formData.append('credit', credit);
    }
    if (!isNaN(cliente) && cliente > 0) {
        formData.append('cliente', cliente);
    }

    // Agregar el resto de los campos
    formData.append('monto', document.getElementById('monto').value);
    formData.append('numero_referencia', document.getElementById('numero_referencia').value);
    formData.append('fecha_emision', document.getElementById('fecha_emision').value);
    formData.append('descripcion', document.getElementById('descripcion').value);
    formData.append('sucursal',document.getElementById('sucursal_id').value);

    // Validar si se seleccionó un archivo
    const archivo = document.getElementById('boleta').files[0];
    if (archivo) {
        formData.append('boleta', archivo);
    } else {
        Swal.fire({
            icon: "error",
            title: `Falta boleta`,
            text: `Debe adjuntar una boleta para continuar.`,
            timer: 3000,
            showConfirmButton: false,
        });
        mostrar(document.getElementById('pago'));
        return;
    }

    // CSRF Token
    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    if (!csrfTokenElement) {
        Swal.fire({
            icon: "error",
            title: `Error de seguridad`,
            text: `Token CSRF no encontrado.`,
            timer: 3000,
            showConfirmButton: false,
        });
        mostrar(document.getElementById('pago'));
        return;
    }

    const csrfToken = csrfTokenElement.getAttribute('content');

    // Enviar el formulario con Axios
    try {
        const response = await axios({
            method: 'post',
            url: urls_p.api_url_pago,
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrfToken
            },
            data: formData
        });

        console.log(response.data);
        Swal.fire({
            icon: "success",
            title: `Registro Completado`,
            text: '¡Formulario enviado con éxito!',
            timer: 3000,
            showConfirmButton: false,
        });
        setTimeout(() => { window.history.back(); }, 1000);

    } catch (error) {
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
            console.error('Error general:', error.message);
            Swal.fire({
                icon: "error",
                title: `Error inesperado`,
                text: error.message,
                timer: 3000,
                showConfirmButton: false,
            });
        }
        mostrar(document.getElementById('pago'));
    }
});
