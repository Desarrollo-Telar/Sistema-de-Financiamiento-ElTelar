import { Desembolso } from '../../class/disbursement.js';

export const desembolso = new Desembolso();

// Función para actualizar el total a depositar
function actualizarTotalDepositar() {
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const poliza_seguro = parseFloat(document.getElementById('poliza_seguro').value) || 0;
    const honorarios = parseFloat(document.getElementById('honorarios').value) || 0;

    // Actualiza los valores en la instancia de Desembolso
    desembolso.monto_credito = monto;
    desembolso.poliza_seguro = poliza_seguro;
    desembolso.honorarios = honorarios;
    desembolso.saldo_anterior = 0; // Ajusta según sea necesario

    // Usa la propiedad total_a_depositar de Desembolso
    const total = desembolso.total_a_depositar;
    
    // Actualiza el valor en el elemento HTML
    document.getElementById('total_depositar').value = Math.round(total);
}

// Agregar event listeners a los campos relevantes
document.getElementById('monto').addEventListener('input', actualizarTotalDepositar);
document.getElementById('poliza_seguro').addEventListener('input', actualizarTotalDepositar);
document.getElementById('honorarios').addEventListener('input', actualizarTotalDepositar);
