import { registrar_desembolso } from '../../API/desembolsos/crear_desembolsos.js';
import { registrar_pago } from '../../API/pagos/crear_pago.js';
import Swal from 'sweetalert2';

async function agregar_desembolso() {
    let formData = new FormData();
    formData.append('credit', document.getElementById('credit').value);
    formData.append('forma_desembolso', 'DESEMBOLSAR');
    formData.append('monto_total_desembolso', document.getElementById('monto').value);
    return await registrar_desembolso(formData);
}

async function agregar_desembolso_pago(disbursement) {
    let formData = new FormData();
    formData.append('disbursement', disbursement);
    formData.append('monto', document.getElementById('monto').value);
    formData.append('numero_referencia', document.getElementById('numero_referencia').value);
    formData.append('fecha_emision', document.getElementById('fecha_emision').value);
    formData.append('descripcion', document.getElementById('descripcion').value);
    formData.append('boleta', document.getElementById('boleta').files[0]);
    return await registrar_pago(formData);
}

document.getElementById('pago').addEventListener('submit', async function (event) {
    event.preventDefault();
    try {
        const register_desembolso = await agregar_desembolso();
        console.log(register_desembolso);

        const register_pago = await agregar_desembolso_pago(register_desembolso.id);
        console.log(register_pago);

        Swal.fire({
            icon: "success",
            title: 'Registro Completado',
            text: '¡Formulario enviado con éxito!',
            timer: 3000,
            showConfirmButton: false,
        });

        setTimeout(() => { window.history.back(); }, 1000);

    } catch (error) {
        console.error('Error al registrar los datos:', error);

        Swal.fire({
            icon: "error",
            title: 'Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.',
            text: `${error}`,
            timer: 3000,
            showConfirmButton: false,
        });
    }
});
