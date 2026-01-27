import {generarLinkPago, generarSaldoActual} from './get_mensaje.js'


document.getElementById('mandar_mensaje').addEventListener('click', () => {
    const cuota = document.getElementById('siguiente_pago').value;
    const cliente = document.getElementById('cliente').value;



    generarLinkPago(cliente,cuota);
    

});

document.getElementById('mandar_mensaje_saldo_actual').addEventListener('click', () => {
    const credito = document.getElementById('saldo_actual_credito').value;

    generarSaldoActual(credito);
    

});