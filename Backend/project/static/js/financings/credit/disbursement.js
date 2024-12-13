import { Desembolso } from '../../class/disbursement.js';
<<<<<<< HEAD
import { urls, urls_p } from '../../API/urls_api.js'
=======
>>>>>>> server
export const desembolso = new Desembolso();
import {urls, urls_p} from '../../API/urls_api.js';

// Variables globales para acumulación y control
let suma = 0, saldo_anterior = 0, credi_id = 0;

// Función para obtener valor numérico de un campo por ID
const obtenerValorNumerico = (id) => parseFloat(document.getElementById(id)?.value) || 0;



// Función para actualizar el total a depositar
async function actualizarTotalDepositar() {
    const monto = obtenerValorNumerico('monto');
<<<<<<< HEAD

    const poliza_seguro = obtenerValorNumerico('poliza_seguro');

    const honorarios = obtenerValorNumerico('honorarios');

    let agg = obtenerValorNumerico('monto_sumar');
    if (desembolso.forma_desembolso == 'CANCELACIÓN DE CRÉDITO VIGENTE' || desembolso.forma_desembolso == 'APLICACIÓN GASTOS') {
        agg = 0;
    }

    const saldo_anterior = obtenerValorNumerico('saldo_anterior');
    const total = monto + agg;


    const total_desembolsar = total - (poliza_seguro + honorarios + saldo_anterior);


    // Actualiza los valores en el objeto desembolso
    desembolso.honorarios = honorarios;
    desembolso.poliza_seguro = poliza_seguro;
    desembolso.monto_credito = total;
    desembolso.saldo_anterior = saldo_anterior;
    desembolso.monto_total_desembolso = total_desembolsar;

    suma = 0;

=======
    const poliza_seguro = obtenerValorNumerico('poliza_seguro');
    const honorarios = obtenerValorNumerico('honorarios');
    const agg = obtenerValorNumerico('monto_sumar');
    const total = monto + agg;

    // Actualiza los valores en el objeto desembolso
    Object.assign(desembolso, { monto_credito: total, poliza_seguro, honorarios, saldo_anterior });

    suma = 0;
    
>>>>>>> server
    try {
        const laboral = await filtro(credi_id);
        
        if (Array.isArray(laboral)) {
            suma = laboral.reduce((acum, el) => acum + parseFloat(el.monto_total_desembolso), 0);
        }

        if (suma >= total_desembolsar) {
            alert('NO SE PUEDE REALIZAR OTRO DESEMBOLSO');
            const addDesembolsoElement = document.getElementById('add_Desembolso');
            if (addDesembolsoElement) {
                addDesembolsoElement.style.display = 'none';
            }
            return;
        }

<<<<<<< HEAD
        document.getElementById('total_depositar').value = parseFloat(total_desembolsar).toFixed(2);
=======
        document.getElementById('total_depositar').value = parseFloat(desembolso.total_a_depositar).toFixed(2);
>>>>>>> server
        const addDesembolsoElement = document.getElementById('add_Desembolso');
        if (addDesembolsoElement) {
            addDesembolsoElement.style.display = '';
        }
    } catch (error) {
        console.error('Error obteniendo detalles del cliente:', error);
    }
}

// Agrega event listeners a los campos relevantes
const campos = ['monto', 'poliza_seguro', 'honorarios', 'monto_sumar', 'saldo_anterior'];
campos.forEach(id => {
    const elemento = document.getElementById(id);
    if (elemento) {
<<<<<<< HEAD

        elemento.addEventListener('input', (event) => {
            //console.log(event.target.value);
            actualizarTotalDepositar();
        });
    }
});


=======
        elemento.addEventListener('input', actualizarTotalDepositar);
    }
});

>>>>>>> server
document.getElementById('desembolso')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
        const credi_id = obtenerValorNumerico('credit_id');
<<<<<<< HEAD
        const desembolsos = await registrarDesembolso(urls.api_url_desembolso, credi_id);
        console.log(desembolsos);

=======
        const desembolsos = await registrarDesembolso(urls_p.api_url_desembolso, credi_id);
        
>>>>>>> server
        alert('¡Formulario enviado con éxito!');
        window.location.href = `/financings/credit/${credi_id}`;
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }
});
<<<<<<< HEAD

// Actualiza el valor en el elemento HTML



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

            const desembolsos = await registrarDesembolso(urls_p.api_url_desembolso, credi_id);
            console.log(desembolsos);
            alert('¡Formulario enviado con éxito!');
            window.location.href = `/financings/credit/${credi_id}`;
        } catch (error) {
            console.error('Error al registrar los datos:', error);
            alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
        }
    });
}
=======
>>>>>>> server


async function registrarDesembolso(url, credit_id) {
    try {
        desembolso.credit_id = credit_id;
        const forma_desembolso = document.getElementById('forma_desembolso');
<<<<<<< HEAD

        if (forma_desembolso) {
            forma_desembolso.addEventListener('change', (event) => {
                const valor_seleccionado = event.target.value;
                if (valor_seleccionado) {
                    desembolso.forma_desembolso = valor_seleccionado;
                    console.log(desembolso.forma_desembolso);

                }
                else {
                    throw new Error('Seleccione una opción');

                }
=======
        
        if (forma_desembolso) {
            forma_desembolso.addEventListener('change', (event) => {
                const valor_seleccionado = event.target.value;
                if (valor_seleccionado) desembolso._forma_desembolso = valor_seleccionado;
                else throw new Error('Seleccione una opción');
>>>>>>> server
            });
        }

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const response = await axios.post(url, desembolso.toJson(), {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error al registrar el desembolso:', error);
        throw error;
    }
}

async function informacionDesembolso() {
<<<<<<< HEAD

    try {
        const response = await fetch(urls.api_url_desembolso);

        if (!response.ok) throw new Error('Error al obtener información de desembolso: ' + response.statusText);

=======
    try {
        const response = await fetch(urls_p.api_url_desembolso);
        
        if (!response.ok) throw new Error('Error al obtener información de desembolso: ' + response.statusText);
        
>>>>>>> server
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener la lista de desembolsos:', error);
        throw error;
    }
<<<<<<< HEAD

    return fetch(urls_p.api_url_desembolso)
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

=======
>>>>>>> server
}

async function filtro(valor) {
    try {
        const desembolsos = await informacionDesembolso();
        return desembolsos.filter(item => item.credit_id === valor);
    } catch (error) {
        console.error('Error en el filtro de desembolsos:', error);
        throw error;
    }
}

document.getElementById('forma_desembolso')?.addEventListener('change', (event) => {
    const valorSeleccionado = event.target.value;
    const divMontoCredito = document.getElementById('div_monto_credito');
    const montoAgregado = document.getElementById('monto_agregado');

    if (!valorSeleccionado) throw new Error('Opción no seleccionada');

    switch (valorSeleccionado) {
        case 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE':
            desembolso.forma_desembolso = valorSeleccionado;
            console.log(desembolso.forma_desembolso);

            // Añade el campo solo si no existe
            if (!montoAgregado) {
                divMontoCredito.innerHTML += `
                    <div class="form-group" style="margin-top: 2rem;" id="monto_agregado">
                        <label class="fw-medium" for="monto_sumar">Monto por agregar</label>
                        <div class="input-group mb-3">
                            <span class="input-group-text fw-medium" id="basic-addon1">Q</span>
                            <input type="number" min="0" step="any" class="form-control" id="monto_sumar">
                        </div>
                    </div>
                `;

                // Añade el listener después de crear el campo
                document.getElementById('monto_sumar').addEventListener('input', actualizarTotalDepositar);
            } else {
                montoAgregado.style.display = 'block';
            }
            break;

        case 'CANCELACIÓN DE CRÉDITO VIGENTE':
            desembolso.forma_desembolso = valorSeleccionado;
            console.log(desembolso.forma_desembolso);

            // Oculta y limpia el campo `monto_sumar` si ya existe
            if (montoAgregado) {
                document.getElementById('monto_sumar').value = ''; // Limpia el valor
<<<<<<< HEAD
                actualizarTotalDepositar();
=======
>>>>>>> server
                montoAgregado.style.display = 'none';
            }
            break;
    }
});

<<<<<<< HEAD

=======
>>>>>>> server
