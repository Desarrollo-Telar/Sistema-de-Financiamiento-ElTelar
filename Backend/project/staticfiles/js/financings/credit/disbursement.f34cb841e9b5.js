import { Desembolso } from '../../class/disbursement.js';
export const desembolso = new Desembolso();
import {urls, urls_p} from '../../API/urls_api.js';

// Variables globales para acumulación y control
let suma = 0, saldo_anterior = 0, credi_id = 0;

// Función para obtener valor numérico de un campo por ID
const obtenerValorNumerico = (id) => parseFloat(document.getElementById(id)?.value) || 0;

// Función para actualizar el total a depositar
async function actualizarTotalDepositar() {
    const monto = obtenerValorNumerico('monto');
    const poliza_seguro = obtenerValorNumerico('poliza_seguro');
    const honorarios = obtenerValorNumerico('honorarios');
    const agg = obtenerValorNumerico('monto_sumar');
    const total = monto + agg;

    // Actualiza los valores en el objeto desembolso
    Object.assign(desembolso, { monto_credito: total, poliza_seguro, honorarios, saldo_anterior });

    suma = 0;
    
    try {
        const laboral = await filtro(credi_id);
        
        if (Array.isArray(laboral)) {
            suma = laboral.reduce((acum, el) => acum + parseFloat(el.monto_total_desembolso), 0);
        }

        if (suma >= total) {
            alert('NO SE PUEDE REALIZAR OTRO DESEMBOLSO');
            const addDesembolsoElement = document.getElementById('add_Desembolso');
            if (addDesembolsoElement) {
                addDesembolsoElement.style.display = 'none';
            }
            return;
        }

        document.getElementById('total_depositar').value = parseFloat(desembolso.total_a_depositar).toFixed(2);
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
        elemento.addEventListener('input', actualizarTotalDepositar);
    }
});

document.getElementById('desembolso')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
        const credi_id = obtenerValorNumerico('credit_id');
        const desembolsos = await registrarDesembolso(urls_p.api_url_desembolso, credi_id);
        
        alert('¡Formulario enviado con éxito!');
        window.location.href = `/financings/credit/${credi_id}`;
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }
});

async function registrarDesembolso(url, credit_id) {
    try {
        desembolso.credit_id = credit_id;
        const forma_desembolso = document.getElementById('forma_desembolso');
        
        if (forma_desembolso) {
            forma_desembolso.addEventListener('change', (event) => {
                const valor_seleccionado = event.target.value;
                if (valor_seleccionado) desembolso._forma_desembolso = valor_seleccionado;
                else throw new Error('Seleccione una opción');
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
    try {
        const response = await fetch(urls_p.api_url_desembolso);
        
        if (!response.ok) throw new Error('Error al obtener información de desembolso: ' + response.statusText);
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener la lista de desembolsos:', error);
        throw error;
    }
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
                montoAgregado.style.display = 'none';
            }
            break;
    }
});

