import {urls_p} from '../../API/urls_api.js';
const url = urls_p.api_url_descuento;

document.getElementById('descuento-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const alertBox = document.getElementById('alert-message');
    alertBox.style.display = 'none';

    const formData = new FormData(this);
    const data = {
        credit: parseInt(formData.get('credit')),
        cuota: parseInt(formData.get('cuota')),
        sucursal: parseInt(formData.get('sucursal')),
        usuario_descuento: parseInt(formData.get('usuario_descuento')),
        interes_por_cobrar: parseFloat(formData.get('interes_por_cobrar')),
        mora_por_cobrar: parseFloat(formData.get('mora_por_cobrar')),
        saldo_capital_por_cobrar: parseFloat(formData.get('saldo_capital_por_cobrar')),
        tipo_descuento: formData.get('tipo_descuento'),
        motivo_descuento: formData.get('motivo_descuento'),
        recalcular_cuota: formData.get('recalcular_cuota') === 'on'
    };

    try {
        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        const csrfToken = csrfTokenElement ? csrfTokenElement.getAttribute('content') : '';
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showAlert('Descuento registrado exitosamente.', 'success');
            this.reset();
            
            let credito = document.getElementById('credit').value;
            setTimeout(() => { window.location.href = `/financings/credit/${credito}`; }, 100);
            
        } else {
            const errorData = await response.json();
            showAlert('Error al guardar: ' + JSON.stringify(errorData), 'error');
        }
    } catch (error) {
        showAlert('Ocurrió un error al procesar la solicitud.', 'error');
        console.error('Error al enviar la solicitud:', error);
    }
});

function showAlert(message, type) {
    const alertBox = document.getElementById('alert-message');
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.style.display = 'block';
}
