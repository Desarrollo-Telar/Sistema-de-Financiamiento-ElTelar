import {urls_p} from '../API/urls_api.js'
import {generarLinkPago} from '../financings/mensaje_alerta/get_mensaje.js'

document.querySelectorAll('.mandar_mensaje').forEach((btn) => {
    btn.addEventListener('click', () => {
        const cuota = btn.getAttribute('data-cuota');
        const cliente = btn.getAttribute('data-cliente');
        generarLinkPago(cliente, cuota);
    });
});



document.querySelectorAll('.ver_recibo').forEach((btn) => {
    btn.addEventListener('click', () => {
        const pagoId = btn.getAttribute('data-id');
        window.location.href = `/financings/recibo/${pagoId}/`;
    });
});

document.querySelectorAll('.editar_cobranza').forEach((btn) => {
    btn.addEventListener('click', () => {
        const cobranzaID = btn.getAttribute('data-id');
        window.location.href = `/customers/asesores_credito/cobranza/actualizar/${cobranzaID}/`;
    });
});

document.querySelectorAll('.ver_historial').forEach((btn) => {
    btn.addEventListener('click', () => {
        const cobranzaID = btn.getAttribute('data-id');
        window.location.href = `/customers/asesores_credito/historial_cobranza/${cobranzaID}/`;
    });
});

