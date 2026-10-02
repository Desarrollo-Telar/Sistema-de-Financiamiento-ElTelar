 
import {urls_p} from '../../API/urls_api.js'

import { get_ultima_cuota_ampliacion } from '../../API/credito/obtener_ultima_cuota.js'
import {get_credit} from '../../API/credito/obtener_credito.js'
import { actualizar_credito } from '../../API/credito/actualizar.js'

// Extendemos select2Data para incluir al 'fiador'
const select2Data = {
    customer: [],
    advisor: [],
    existing_credit: [],
    fiador: []
};


// Declaración de variables para debounce y selección de créditos
let searchTimeout = null;
let existingCreditsSearchTimeout = null;
const selectedCreditsMap = new Map();

// Para enviar solo los IDs al backend:
const selectedIds = Array.from(selectedCreditsMap.keys()); 
// ["105", "204", "311"]

// Para enviar los objetos completos:
const selectedObjects = Array.from(selectedCreditsMap.values());



window.searchExistingCredits = function() {

    clearTimeout(existingCreditsSearchTimeout);

    const input = document.getElementById(
        'existing_credit_search'
    );

    if (!input) {
        return;
    }

    const term = input.value.trim();


    existingCreditsSearchTimeout = setTimeout(() => {

        loadExistingCredits(term);

    }, 250);
};


window.searchSelect2 = function(type) {

    clearTimeout(searchTimeout);

    const input = document.getElementById(
        `${type}_search_input`
    );

    if (!input) {
        return;
    }

    const term = input.value.trim();

    searchTimeout = setTimeout(() => {

        loadSelect2Data(type, term);

    }, 250);
};

// Abrir dropdown
window.openSelect2 = function(type) {

    document.querySelectorAll('.select2-dropdown').forEach(el => {
        el.classList.add('hidden');
    });

    const dropdown = document.getElementById(`${type}_dropdown`);

    if (!dropdown) {
        console.error(`No existe: ${type}_dropdown`);
        return;
    }

    dropdown.classList.remove('hidden');

    // Cargar información
    loadSelect2Data(type);
}

window.selectSelect2Option = async function(type, id, text) {

    const searchInput =
        document.getElementById(`${type}_search_input`);

    const dropdown =
        document.getElementById(`${type}_dropdown`);

    if (!searchInput || !dropdown) {
        console.error(`No se encontraron elementos para ${type}`);
        return;
    }


    // Mostrar texto seleccionado
    searchInput.value = text;


    // Determinar input hidden
    let hiddenInputId;

    if (type === 'customer') {

        hiddenInputId = 'customer_id';

    } else if (type === 'advisor') {

        hiddenInputId = 'asesor_de_credito';

    } else if (type === 'existing_credit') {

        hiddenInputId = 'credito_vigente';

    }


    const hiddenInput =
        document.getElementById(hiddenInputId);


    if (hiddenInput) {
        hiddenInput.value = id;
    }


    // Cerrar dropdown
    dropdown.classList.add('hidden');


    // Si seleccionó un crédito vigente
    if (type === 'existing_credit') {

        await seleccionarCreditoVigente(id);

    }
};


// Obtener datos desde API
async function loadSelect2Data(type, term = '') {
    let url;

    if (type === 'customer' || type === 'fiador') {
        url = `${urls_p.api_url_cliente || urls_p.api_url_clientes_aceptados}?term=${encodeURIComponent(term)}`;
    } else if (type === 'advisor') {
        url = `${urls_p.api_url_asesores_credito}?term=${encodeURIComponent(term)}`;
    } else if (type === 'existing_credit') {
        url = `${urls_p.api_url_credit_vigente}?term=${encodeURIComponent(term)}`;
    } else {
        return;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        if (type === 'customer' || type === 'fiador') {
            select2Data[type] = data.map(item => ({
                id: item.id,
                text: `${item.customer_code} ${item.first_name} ${item.last_name}`,
                raw: item
            }));
        }
        // ASESORES
        else if (type === 'advisor') {

            select2Data.advisor = data.map(item => ({
                id: item.id,
                text: `${item.nombre} ${item.apellido}`
            }));

        }


        // CRÉDITOS VIGENTES
        else if (type === 'existing_credit') {

            select2Data.existing_credit = data.map(item => ({

                id: item.id,

                text:
                    `${item.sucursal.nombre} - ` +
                    `${item.codigo_credito} ` +
                    `${item.customer_id.first_name} ` +
                    `${item.customer_id.last_name}`

            }));

        }
        
        renderSelect2Options(type);
    } catch (error) {
        console.error(`Error cargando ${type}:`, error);
        select2Data[type] = [];
        renderSelect2Options(type);
    }
}


 
window.loadExistingCredits  =  async function(term = '') {
    const container = document.getElementById('existing-credits-list');
    if (!container) return;

    const query = term.trim();

    // Evitar consultar si no se escribió nada
    if (!query) {
        container.innerHTML = `
            <div class="p-3 text-xs text-brandGrayText text-center">
                Escriba un código, nombre o apellido para buscar créditos vigentes
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="p-3 text-xs text-brandGrayText text-center">
            Buscando créditos...
        </div>
    `;

    try {
        const url = `${urls_p.api_url_credit_vigente}?term=${encodeURIComponent(query)}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data)) {
            console.error('Estructura de datos inesperada:', data);
            renderExistingCredits([]);
            return;
        }

        renderExistingCredits(data);

    } catch (error) {
        console.error('Error buscando créditos vigentes:', error);
        container.innerHTML = `
            <div class="p-3 text-xs text-red-600 text-center">
                Error al consultar los créditos
            </div>
        `;
    }
}





// Quitar un crédito desde la "pilla" o etiqueta de arriba
window.removeCreditSelection = function(id) {
    selectedCreditsMap.delete(String(id));
    
    // Renderizar chips actualizados
    renderSelectedChips();

    // Sincronizar el checkbox si la búsqueda actual contiene ese crédito
    const searchInput = document.getElementById('existing_credit_search');
    if (searchInput && searchInput.value.trim() !== '') {
        loadExistingCredits(searchInput.value);
    }
}




async function seleccionarCreditoVigente(creditoId) {

    try {

        // Obtener toda la información relacionada
        // con el crédito vigente seleccionado
        const credito_v = await get_credit(creditoId);


        if (credito_v.id == 1) {

            const formData = new FormData();

            formData.append(
                'is_paid_off',
                false
            );

            actualizar_credito(
                credito_v.id,
                formData
            );
        }


        // Obtener la última cuota vigente
        const cuotas =
            await get_ultima_cuota_ampliacion(
                credito_v.id
            );


        const cuota = cuotas[0];


        // Mostrar información del crédito
        const informacion_credito =
            document.getElementById(
                'informacion_credito'
            );


        informacion_credito.style.display = 'block';


        informacion_credito.innerHTML = `
            <p>
                Saldo Capital Pendiente:
                ${cuota.saldo_pendiente}
            </p>

            <p>
                Intereses:
                ${cuota.interest}
            </p>

            <p>
                Mora:
                ${cuota.mora}
            </p>

            <p>
                Plazo del Crédito:
                ${credito_v.plazo} Meses
            </p>

            <hr>

            <p>
                Saldo Actual:
                ${credito_v.Fsaldo_actual}
            </p>
        `;


        // Mostrar campos relacionados
        mostrar(monto_credito_vigente);
        mostrar(saldo_capital_credito_vigente);
        mostrar(honorarios_desembolso);
        mostrar(poliza_seguro_desembolso);
        mostrar(monto_desembolsado_desembolsar);
        mostrar(total_a_desembolsar);


        // Asignar valores
        document.getElementById(
            'credito_monto_vigente'
        ).value = credito_v.monto;


        document.getElementById(
            'credito_saldo_capital_vigente'
        ).value = credito_v.saldo_actual;


        // Recalcular total
        actualizarTotalDepositar();


    } catch (error) {

        console.error(
            'Error obteniendo detalles del crédito:',
            error
        );

    }
}

// Función para renderizar los resultados que devuelve la API
function renderExistingCredits(creditsList) {
    const container = document.getElementById('existing-credits-list');
    if (!container) return;

    if (creditsList.length === 0) {
        container.innerHTML = `
            <div class="p-3 text-xs text-brandGrayText text-center">
                No se encontraron créditos vigentes
            </div>
        `;
        return;
    }

    container.innerHTML = '';

    creditsList.forEach(credit => {
        const creditIdStr = String(credit.id);
        const isChecked = selectedCreditsMap.has(creditIdStr);

        const item = document.createElement('label');
        item.className = `flex items-center justify-between p-2 mb-1 rounded cursor-pointer transition-colors ${
            isChecked ? 'bg-amber-500/10' : 'hover:bg-white/10'
        }`;

        // Escapamos comillas simples para evitar errores al pasar el JSON
        const creditJson = JSON.stringify(credit).replace(/'/g, "&apos;");

        item.innerHTML = `
            <div class="flex items-center gap-2">
                <input type="checkbox" 
                       value="${credit.id}" 
                       ${isChecked ? 'checked' : ''} 
                       onchange='toggleCreditSelection(this, ${creditJson})'
                       class="glass-checkbox">
                <span class="text-xs font-semibold">${credit.sucursal.nombre} - ${credit.codigo_credito}  </span>
                <span class="text-xs opacity-75">${credit.customer_id.first_name} ${credit.customer_id.last_name}</span>
            </div>
            <span class="text-xs font-mono">Q${credit.Fsaldo_actual || credit.monto || 0}</span>
        `;
        container.appendChild(item);
    });
}


// Pintar opciones
function renderSelect2Options(type) {

    const dropdown = document.getElementById(`${type}_dropdown`);

    if (!dropdown) {
        console.error(`No existe: ${type}_dropdown`);
        return;
    }

    const data = select2Data[type] || [];


    if (data.length === 0) {

        dropdown.innerHTML = `
            <div class="p-3 text-xs text-brandGrayText text-center">
                No se encontraron resultados
            </div>
        `;

        return;
    }


    dropdown.innerHTML = data.map(item => {

        const id = String(item.id)
            .replace(/'/g, "\\'");

        const text = String(item.text)
            .replace(/'/g, "\\'");

        return `
            <div
                class="select2-option"
                onclick="selectSelect2Option(
                    '${type}',
                    '${id}',
                    '${text}'
                )"
            >
                ${item.text}
            </div>
        `;

    }).join('');
}

// Marcar o desmarcar un crédito
window.toggleCreditSelection = function(checkbox, creditObj) {
    const creditIdStr = String(creditObj.id);

    if (checkbox.checked) {
        selectedCreditsMap.set(creditIdStr, creditObj);
    } else {
        selectedCreditsMap.delete(creditIdStr);
    }

    renderSelectedChips();
}


// Dibujar las etiquetas acumuladas arriba de la lista
function renderSelectedChips() {
    const chipsContainer = document.getElementById('selected-credits-chips');
    if (!chipsContainer) return;

    chipsContainer.innerHTML = '';

    selectedCreditsMap.forEach((credit, id) => {
        const chip = document.createElement('span');
        chip.className = 'badge badge-amber flex items-center gap-1 text-xs py-1 px-2';
        chip.innerHTML = `
            <span>${credit.sucursal.nombre } - ${credit.codigo_credito  } - ${credit.customer_id.first_name} ${credit.customer_id.last_name}</span>
            <i class="fa-solid fa-xmark cursor-pointer ml-1 hover:text-red-400" 
               onclick="removeCreditSelection('${id}')"></i>
        `;
        chipsContainer.appendChild(chip);
    });
}


// --- BÚSQUEDA LABORAL DE FIADOR ---
async function fetchInformacionLaboral(clienteId) {
    try {
        const response = await fetch(`${urls_p.api_url_informacion_laboral}?term=${clienteId}`);
        return response.ok ? await response.json() : [];
    } catch (e) {
        return [];
    }
}

async function fetchOtraInformacionLaboral(clienteId) {
    try {
        const response = await fetch(`${urls_p.api_url_otra_informacion_laboral}?term=${clienteId}`);
        return response.ok ? await response.json() : [];
    } catch (e) {
        return [];
    }
}

export async function buscarFiadorLaboral(clienteId) {
    const laboral = await fetchInformacionLaboral(clienteId);
    const otra = await fetchOtraInformacionLaboral(clienteId);

    let filterList = [];

    const getCustomerId = (item) => (typeof item.customer_id === 'object' ? item.customer_id.id : item.customer_id);

    if (laboral && laboral.length > 0) {
        filterList = laboral.filter(item => getCustomerId(item) === clienteId);
    }

    if (filterList.length === 0 && otra && otra.length > 0) {
        filterList = otra.filter(item => getCustomerId(item) === clienteId);
    }

    return filterList;
}



// Lógica de selección para autocompletar automáticamente el Fiador
window.selectSelect2Option = async function(type, id, text) {
    const searchInput = document.getElementById(`${type}_search_input`);
    const dropdown = document.getElementById(`${type}_dropdown`);

    if (searchInput) searchInput.value = text;
    if (dropdown) dropdown.classList.add('hidden');

    if (type === 'fiador') {
        document.getElementById('json_fiador_customer_id').value = id;

        try {
            // 1. Obtener detalles del cliente
            const resClient = await fetch(`${urls_p.api_url_cliente}${id}/`);
            if (resClient.ok) {
                const cliente = await resClient.json();
                document.getElementById('json_fiador_codigo').value = cliente.customer_code || '';
                document.getElementById('json_fiador_nombre').value = `${cliente.first_name} ${cliente.last_name}`;
                document.getElementById('json_fiador_tel').value = cliente.telephone || '';
                document.getElementById('json_fiador_foto').value = cliente.photo || '';
            }

            // 2. Obtener y auto-completar datos de información laboral
            const laboral = await buscarFiadorLaboral(id);
            if (laboral.length > 0) {
                const info = laboral[0];
                document.getElementById('json_fiador_trabajo').value = info.company_name || info.source_of_income || '';
                document.getElementById('json_fiador_ingreso').value = info.salary || 0;
            } else {
                document.getElementById('json_fiador_trabajo').value = 'N/A';
                document.getElementById('json_fiador_ingreso').value = 0;
            }
        } catch (error) {
            console.error('Error al autocompletar el fiador:', error);
        }
    }
};