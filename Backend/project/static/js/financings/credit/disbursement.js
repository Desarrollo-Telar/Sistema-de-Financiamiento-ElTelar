import { Desembolso } from '../../class/disbursement.js';

export const desembolso = new Desembolso();

// Función para actualizar el total a depositar
function actualizarTotalDepositar() {
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const poliza_seguro = parseFloat(document.getElementById('poliza_seguro').value) || 0;
    const honorarios = parseFloat(document.getElementById('honorarios').value) || 0;
    const saldo_anterior = parseFloat(document.getElementById('saldo_anterior').value) || 0;

    // Actualiza los valores en la instancia de Desembolso
    desembolso.monto_credito = monto;
    desembolso.poliza_seguro = poliza_seguro;
    desembolso.honorarios = honorarios;
    desembolso.saldo_anterior = saldo_anterior; // Ajusta según sea necesario

    // Usa la propiedad total_a_depositar de Desembolso
    const total = desembolso.total_a_depositar;
    
    // Actualiza el valor en el elemento HTML
    document.getElementById('total_depositar').value = Math.round(total);
}

// Agregar event listeners a los campos relevantes
document.getElementById('monto').addEventListener('input', actualizarTotalDepositar);
document.getElementById('poliza_seguro').addEventListener('input', actualizarTotalDepositar);
document.getElementById('honorarios').addEventListener('input', actualizarTotalDepositar);

document.getElementById('desembolso').addEventListener('submit', async function (event) {
    event.preventDefault();
    try {
        const credi_id = document.getElementById('credit_id').value;

       
        const desembolsos = await registrarDesembolso('http://127.0.0.1:8000/financings/api/desembolso/',credi_id);
        console.log(desembolsos)
        alert('¡Formulario enviado con éxito!');
        window.location.href = '/financings/disbursement/';


    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }
});

async function registrarDesembolso(url, credit_id){
    try {
        desembolso.credit_id = credit_id

        

        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) {
            throw new Error('CSRF token not found');
        }
        const csrfToken = csrfTokenElement.getAttribute('content');

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(desembolso.toJson())
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }

}