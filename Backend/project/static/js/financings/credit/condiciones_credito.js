import {urls_p} from '../../API/urls_api.js'

const API_URL = urls_p.api_url_condiciones_credito;
const CREDIT_ID = document.getElementById('credit').value;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', cargarCondiciones);

async function cargarCondiciones() {
    try {
        const response = await fetch(`${API_URL}?credit=${CREDIT_ID}`);
        const data = await response.json();

        const tbody = document.getElementById('tablaCondiciones');
        tbody.innerHTML = '';

        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted py-4">No hay condiciones registradas para este crédito.</td></tr>`;
            return;
        }

        data.forEach(item => {
            tbody.innerHTML += `
                    <tr>
                        <td class="ps-4"><strong>${item.reglas}</strong></td>
                        <td>Q${parseFloat(item.monto).toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                        <td class="text-end pe-4">
                            <button class="btn btn-sm btn-outline-dark me-1" onclick="cargarParaEditar(${item.id}, '${item.reglas}', '${item.monto}')">Editar</button>
                            <button class="btn btn-sm btn-outline-red" onclick="eliminarCondicion(${item.id})">Eliminar</button>
                        </td>
                    </tr>
                `;
        });
    } catch (error) {
        mostrarError('Error al sincronizar las condiciones.');
    }
}

document.getElementById('condicionForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    ocultarAlerta();

    const id = document.getElementById('condicion_id').value;
    const reglas = document.getElementById('reglas').value;
    const monto = document.getElementById('monto').value;

    const payload = {
        credit: parseInt(CREDIT_ID),
        reglas: reglas,
        monto: parseFloat(monto)
    };

    const esEdicion = id !== "";
    const url = esEdicion ? `${API_URL}${id}/` : API_URL;
    const method = esEdicion ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            let mensaje = "Ocurrió un error al guardar la regla.";
            if (typeof result === 'object') {
                mensaje = Object.values(result).flat().join(' ');
            }
            mostrarError(mensaje);
            return;
        }

        resetearFormulario();
        cargarCondiciones();
    } catch (error) {
        mostrarError('Error de red al intentar guardar.');
    }
});

function cargarParaEditar(id, regla, monto) {
    document.getElementById('condicion_id').value = id;
    document.getElementById('reglas').value = regla;
    document.getElementById('monto').value = monto;

    document.getElementById('formTitle').innerText = 'Editar Condición';
    document.getElementById('btnGuardar').innerText = 'Actualizar Condición';
    document.getElementById('btnCancelar').classList.remove('d-none');
}

async function eliminarCondicion(id) {
    if (!confirm('¿Deseas eliminar esta condición del crédito?')) return;

    try {
        const response = await fetch(`${API_URL}${id}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': csrftoken }
        });

        if (response.ok) {
            cargarCondiciones();
        } else {
            mostrarError('No se pudo eliminar el registro.');
        }
    } catch (error) {
        mostrarError('Error de conexión al eliminar.');
    }
}

function resetearFormulario() {
    document.getElementById('condicionForm').reset();
    document.getElementById('condicion_id').value = '';
    document.getElementById('formTitle').innerText = 'Registrar Condición';
    document.getElementById('btnGuardar').innerText = 'Guardar Condición';
    document.getElementById('btnCancelar').classList.add('d-none');
    ocultarAlerta();
    
}

function mostrarError(mensaje) {
    const alertBox = document.getElementById('apiAlert');
    document.getElementById('alertMessage').innerText = mensaje;
    alertBox.classList.remove('d-none');
}

function ocultarAlerta() {
    document.getElementById('apiAlert').classList.add('d-none');
}
