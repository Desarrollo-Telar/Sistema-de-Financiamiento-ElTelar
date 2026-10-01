import {urls_p} from '../../API/urls_api.js'

const select2Data = {
    customer: [],
    advisor: [],
    existing_credit: []
};

let searchTimeout = null;
let activeTab = 'credito';

let existingCreditsSearchTimeout = null;

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
async function loadExistingCredits(term = '') {

    const container = document.getElementById(
        'existing-credits-list'
    );

    if (!container) {
        return;
    }


    // Evitar consultar si no se escribió nada
    if (!term) {

        container.innerHTML = `
            <div class="p-3 text-xs text-brandGrayText text-center">
                Escriba un código, sucursal o titular para buscar
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

        const url =
            `${urls_p.api_url_credit_vigente}?term=${encodeURIComponent(term)}`;


        const response = await fetch(url);


        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }


        const data = await response.json();


        if (!Array.isArray(data)) {

            console.error(
                'Estructura de datos inesperada:',
                data
            );

            renderExistingCredits([]);

            return;
        }


        renderExistingCredits(data);


    } catch (error) {

        console.error(
            'Error buscando créditos vigentes:',
            error
        );


        container.innerHTML = `
            <div class="p-3 text-xs text-red-600 text-center">
                Error al consultar los créditos
            </div>
        `;
    }
}
function renderExistingCredits(credits) {

    const container =
        document.getElementById(
            'existing-credits-list'
        );


    if (!container) {
        return;
    }


    if (credits.length === 0) {

        container.innerHTML = `
            <div class="p-3 text-xs text-brandGrayText text-center">
                No hay créditos coincidentes
            </div>
        `;

        return;
    }


    container.innerHTML = credits.map(c => `

        <label
            class="flex items-center justify-between
                   p-2.5 rounded-xl
                   bg-white
                   hover:bg-amber-100/50
                   border border-brandGrayBorder/60
                   cursor-pointer
                   text-xs
                   transition-colors"
        >

            <div class="flex items-center space-x-3">

                <input
                    type="checkbox"
                    value="${c.id}"
                    data-total-pendiente="${c.total_pendiente || 0}"
                    onchange="calculateDisbursementTotals()"
                    class="existing-credit-chk
                           rounded
                           border-brandGrayBorder
                           text-brandRed
                           focus:ring-brandRed
                           w-4 h-4"
                >

                <div>

                    <span class="font-bold text-darkCard">
                        ${c.codigo_credito}
                    </span>

                    <span class="text-brandGrayText">
                        (${c.sucursal.nombre})
                        -
                        ${c.customer_id.first_name}
                        ${c.customer_id.last_name}
                    </span>

                </div>

            </div>


            <div class="text-right font-mono">

                <span class="text-amber-700 font-bold">
                    Q ${Number(c.total_pendiente || 0).toFixed(2)}
                </span>

                <span class="block text-[10px] text-brandGrayText">
                    Capital:
                    Q${Number(c.saldo_capital || 0).toFixed(2)}
                </span>

            </div>

        </label>

    `).join('');
}

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


// Obtener datos desde API
async function loadSelect2Data(type, term = '') {

    let url;

    if (type === 'customer') {

        url = `${urls_p.api_url_clientes_aceptados}?term=${encodeURIComponent(term)}`;

    } else if (type === 'advisor') {

        url = `${urls_p.api_url_asesores_credito}?term=${encodeURIComponent(term)}`;

    } else if (type === 'existing_credit') {

        url = `${urls_p.api_url_credit_vigente}?term=${encodeURIComponent(term)}`;

    } else {
        return;
    }

    try {

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data)) {
            console.error('Estructura de datos inesperada:', data);
            select2Data[type] = [];
            renderSelect2Options(type);
            return;
        }


        // CLIENTES
        if (type === 'customer') {

            select2Data.customer = data.map(item => ({
                id: item.id,
                text: `${item.customer_code} ${item.first_name} ${item.last_name}`
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


// Seleccionar opción
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

window.switchTab = function (tabId) {
    activeTab = tabId;
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('tab-active');
        btn.classList.add('text-brandGrayText');
    });

    document.getElementById(`tab-${tabId}`).classList.remove('hidden');
    const activeBtn = document.getElementById(`tab-btn-${tabId}`);
    activeBtn.classList.add('tab-active');
    activeBtn.classList.remove('text-brandGrayText');

    if (tabId === 'plan') {
        generatePaymentPlan();
    }
}

window.toggleGracePeriod = function () {
    const formaPago = document.getElementById('forma_de_pago').value;
    const graceInput = document.getElementById('plazo_gracia');

    if (formaPago === 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO' || formaPago === 'INTERES Y CAPITAL AL VENCIMIENTO') {
        graceInput.disabled = false;
        if (parseInt(graceInput.value) === 0) graceInput.value = 3;
    } else {
        graceInput.disabled = true;
        graceInput.value = 0;
    }
    calculateDatesAndBalances();
}

window.calculateDatesAndBalances = function () {
    const fechaInicioVal = document.getElementById('fecha_inicio').value;
    const plazoMeses = parseInt(document.getElementById('plazo').value) || 0;
    const plazoGracia = parseInt(document.getElementById('plazo_gracia').value) || 0;
    const monto = parseFloat(document.getElementById('monto').value) || 0;

    if (fechaInicioVal) {
        const startDate = new Date(fechaInicioVal + 'T00:00:00');

        // Expiration Date = Start Date + plazo
        const expDate = new Date(startDate);
        expDate.setMonth(expDate.getMonth() + plazoMeses);
        document.getElementById('fecha_vencimiento').value = expDate.toLocaleDateString('es-GT', { year: 'numeric', month: '2-digit', day: '2-digit' });

        // Grace Date = Start Date + plazo_gracia
        if (plazoGracia > 0 && !document.getElementById('plazo_gracia').disabled) {
            const graceDate = new Date(startDate);
            graceDate.setMonth(graceDate.getMonth() + plazoGracia);
            document.getElementById('fecha_finalizacion_gracia').value = graceDate.toLocaleDateString('es-GT', { year: 'numeric', month: '2-digit', day: '2-digit' });
        } else {
            document.getElementById('fecha_finalizacion_gracia').value = 'N/A';
        }
    }

    document.getElementById('bg_saldo_pendiente').textContent = `Q ${monto.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    document.getElementById('bg_plazo_restante').textContent = `${plazoMeses} meses`;
    document.getElementById('summary_monto_credito').textContent = `Q ${monto.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

    calculateDisbursementTotals();
}


window.calculateDisbursementTotals = function () {

    const montoCredito =
        parseFloat(document.getElementById('monto')?.value) || 0;

    const honorarios =
        parseFloat(document.getElementById('honorarios')?.value) || 0;

    const poliza =
        parseFloat(document.getElementById('poliza_seguro')?.value) || 0;

    const montoDesembolsado =
        parseFloat(document.getElementById('monto_desembolsado')?.value) || 0;


    // ==========================================================
    // SALDO ANTERIOR DE LOS CRÉDITOS SELECCIONADOS
    // ==========================================================

    let saldoAnterior = 0;

    document
        .querySelectorAll(
            '#existing-credits-list .existing-credit-chk:checked'
        )
        .forEach(chk => {

            const saldoPendiente =
                parseFloat(
                    chk.dataset.totalPendiente
                ) || 0;

            saldoAnterior += saldoPendiente;
        });


    // ==========================================================
    // TOTAL DE GASTOS
    // ==========================================================

    const totalGastos =
        honorarios + poliza;


    // ==========================================================
    // DIFERENCIA DEL DESEMBOLSO
    //
    // Monto crédito -
    // (saldo anterior + póliza + honorarios + monto desembolsado)
    // ==========================================================

    const montoTotalDesembolsoDiferencia =
        montoCredito -
        (
            saldoAnterior +
            poliza +
            honorarios +
            montoDesembolsado
        );


    // ==========================================================
    // FORMATEAR VALORES
    // ==========================================================

    const formatoMoneda = valor =>
        `Q ${valor.toLocaleString('es-GT', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })}`;


    // ==========================================================
    // ACTUALIZAR RESUMEN
    // ==========================================================

    document.getElementById('summary_monto_credito').textContent =
        formatoMoneda(montoCredito);

    document.getElementById('summary_saldo_anterior').textContent =
        formatoMoneda(saldoAnterior);

    document.getElementById('summary_honorarios').textContent =
        formatoMoneda(honorarios);

    document.getElementById('summary_poliza').textContent =
        formatoMoneda(poliza);

    document.getElementById('summary_monto_desembolsado').textContent =
        formatoMoneda(montoDesembolsado);

    document.getElementById('summary_total_gastos').textContent =
        formatoMoneda(totalGastos);


    // ==========================================================
    // DIFERENCIA
    // ==========================================================

    const difDisplay =
        document.getElementById('summary_diferencia');

    const statusMsg =
        document.getElementById('summary_status_msg');


    difDisplay.textContent =
        formatoMoneda(montoTotalDesembolsoDiferencia);


    // ==========================================================
    // ESTADO DEL DESGLOSE
    // ==========================================================

    if (Math.abs(montoTotalDesembolsoDiferencia) < 0.01) {

        // Cuadra exactamente
        difDisplay.className =
            'text-lg font-bold font-mono text-emerald-600';

        statusMsg.textContent =
            '✓ El desglose cuadra exactamente con el crédito.';

        statusMsg.className =
            'text-[11px] text-emerald-600 font-medium';

    }

    else if (montoTotalDesembolsoDiferencia > 0) {

        // Existe dinero que todavía no ha sido asignado
        difDisplay.className =
            'text-lg font-bold font-mono text-amber-600';

        statusMsg.textContent =
            `⚠️ Sobrante sin asignar de Q ${montoTotalDesembolsoDiferencia.toLocaleString(
                'es-GT',
                {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }
            )}`;

        statusMsg.className =
            'text-[11px] text-amber-600 font-medium';

    }

    else {

        // Se está asignando más dinero del disponible
        difDisplay.className =
            'text-lg font-bold font-mono text-red-600';

        statusMsg.textContent =
            `❌ Exceso asignado de Q ${Math.abs(
                montoTotalDesembolsoDiferencia
            ).toLocaleString(
                'es-GT',
                {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }
            )}`;

        statusMsg.className =
            'text-[11px] text-red-600 font-medium';
    }
};

window.toggleDisbursementMode = function () {
    const mode = document.getElementById('forma_desembolso').value;
    const panel = document.getElementById('existing-credits-panel');

    if (mode === 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE' || mode === 'CANCELACIÓN DE CRÉDITO VIGENTE') {
        panel.classList.remove('hidden');
    } else {
        panel.classList.add('hidden');
        document.querySelectorAll('.existing-credit-chk').forEach(chk => chk.checked = false);
    }
    calculateDisbursementTotals();
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