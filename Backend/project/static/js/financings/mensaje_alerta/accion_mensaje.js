import {generarLinkPago} from './get_mensaje.js'


document.getElementById('mandar_mensaje').addEventListener('click', () => {
    const cuota = document.getElementById('siguiente_pago').value;
    const cliente = document.getElementById('cliente').value;

    console.log(cliente);
    console.log(cuota);

    generarLinkPago(cliente,cuota);
    

});