import { Desembolso } from '../../class/disbursement.js';

export const desembolso = new Desembolso();

// Variables globales para acumulación y control
var suma = 0;
var saldo_anterior = 0;
var credi_id = 0;

// Función para actualizar el total a depositar
async function actualizarTotalDepositar() {
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const poliza_seguro = parseFloat(document.getElementById('poliza_seguro').value) || 0;
    const honorarios = parseFloat(document.getElementById('honorarios').value) || 0;

    if (document.getElementById('saldo_anterior')) {
        saldo_anterior = parseFloat(document.getElementById('saldo_anterior').value) || 0;
    }
    if (document.getElementById('credit_id')) {
        credi_id = parseInt(document.getElementById('credit_id').value) || 0;
    }

    // Actualiza los valores en la instancia de Desembolso
    desembolso.monto_credito = monto;
    desembolso.poliza_seguro = poliza_seguro;
    desembolso.honorarios = honorarios;
    desembolso.saldo_anterior = saldo_anterior;

    suma = 0;
    const total = desembolso.total_a_depositar;

    try {
        const laboral = await filtro(credi_id);

        if (Array.isArray(laboral)) {
            laboral.forEach(element => {
                suma += parseFloat(element['monto_total_desembolso']);
            });
        }

        if (suma >= total) {
            alert('NO SE PUEDE REALIZAR OTRO DESEMBOLSO');
            if (document.getElementById('add_Desembolso')) {
                document.getElementById('add_Desembolso').style.display = 'none';
            }
            return;
        }

        console.log('Suma total de desembolsos:', suma);
    } catch (error) {
        console.error('Error obteniendo detalles del cliente:', error);
    }
    if (document.getElementById('add_Desembolso')) {
        document.getElementById('add_Desembolso').style.display = '';
    }
    

    // Actualiza el valor en el elemento HTML
    document.getElementById('total_depositar').value = Math.round(total);
}

// Agregar event listeners a los campos relevantes
document.getElementById('monto').addEventListener('input', actualizarTotalDepositar);
document.getElementById('poliza_seguro').addEventListener('input', actualizarTotalDepositar);
document.getElementById('honorarios').addEventListener('input', actualizarTotalDepositar);
if (document.getElementById('saldo_anterior')) {
    document.getElementById('saldo_anterior').addEventListener('input', actualizarTotalDepositar);
}

if (document.getElementById('desembolso')) {
    document.getElementById('desembolso').addEventListener('submit', async function (event) {
        event.preventDefault();
        try {
            const credi_id = parseInt(document.getElementById('credit_id').value);
    
            const desembolsos = await registrarDesembolso('http://127.0.0.1:8000/financings/api/desembolso/', credi_id);
            console.log(desembolsos);
            alert('¡Formulario enviado con éxito!');
            window.location.href = `/financings/credit/${credi_id}`;
        } catch (error) {
            console.error('Error al registrar los datos:', error);
            alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
        }
    });
}

async function registrarDesembolso(url, credit_id) {
    try {
        desembolso.credit_id = credit_id;

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await axios.post(url, desembolso.toJson(), {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        alert('Error: ',error);
        console.error('Error al registrar el desembolso:', error);
        throw error;
    }
}


async function informacionDesembolso() {
    return fetch('http://127.0.0.1:8000/financings/api/desembolso/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener información de desembolso: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Lista de desembolsos obtenida:', data);
            return data;
        })
        .catch(error => {
            console.error('Error al obtener la lista de desembolsos:', error);
            throw error;
        });
}

async function filtro(valor) {
    try {
        const desembolso = await informacionDesembolso();
        let filterList = [];

        if (desembolso && Array.isArray(desembolso) && desembolso.length > 0) {
            filterList = desembolso.filter(item => item['credit_id'] === valor);
        }

        console.log(filterList);
        return filterList;
    } catch (error) {
        console.error('Error en el filtro de desembolsos:', error);
        throw error;
    }
}
