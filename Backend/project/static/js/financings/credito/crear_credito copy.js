
// Data Sources (Mock Records for Searchable Select2 Component)
const mockCustomers = [
    { id: 1, text: 'CLI-8821 - Juan Luis Melchor Reyes (DPI: 2341 88412 0101)' },
    { id: 2, text: 'CLI-4410 - María Mercedes López (DPI: 1822 90123 1601)' },
    { id: 3, text: 'CLI-9012 - Agropecuaria El Sol S.A. (NIT: 882194-1)' },
    { id: 4, text: 'CLI-5102 - Carlos Alberto Morales (DPI: 2991 33410 0901)' },
    { id: 5, text: 'CLI-1029 - Importadora La Bendición S.A. (NIT: 771239-0)' }
];

const mockAdvisors = [
    { id: 'Lic. Carlos Mendoza', text: 'Lic. Carlos Mendoza - Asesor Senior Central' },
    { id: 'Ing. Ana Sofía Ramírez', text: 'Ing. Ana Sofía Ramírez - Asesor Agrícola Norte' },
    { id: 'Lcda. Beatriz Morales', text: 'Lcda. Beatriz Morales - Asesora PYME' },
    { id: 'Ing. Roberto Fuentes', text: 'Ing. Roberto Fuentes - Asesor Microcréditos' }
];

const mockExistingCredits = [
    { id: 'CRED-2024-001', sucursal: 'OFICINA 1', saldo_capital: 3000.00, interes: 262.00, total_pendiente: 3262.00, titular: 'JUAN LUIS MELCHOR' },
    { id: 'CRED-2023-089', sucursal: 'OFICINA 1', saldo_capital: 1500.00, interes: 120.00, total_pendiente: 1620.00, titular: 'JUAN LUIS MELCHOR' },
    { id: 'CRED-2022-104', sucursal: 'OFICINA CENTRAL', saldo_capital: 8000.00, interes: 450.00, total_pendiente: 8450.00, titular: 'JUAN LUIS MELCHOR' },
    { id: 'CRED-2024-055', sucursal: 'SUCURSAL NORTE', saldo_capital: 4200.00, interes: 180.00, total_pendiente: 4380.00, titular: 'JUAN LUIS MELCHOR' }
];

// State variables
let guaranteeList = [];
let activeTab = 'credito';

function getStorageData(key) {
  try {
    return localStorage.getItem(key);
  } catch (e) {
    console.warn('Storage no accesible:', e);
    return null;
  }
}

// 1. Definir explícitamente en window para que onclick="..." las encuentre siempre
  window.switchTab = function(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.remove('hidden');
  };

  window.openSelect2 = function(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
      const dropdown = container.querySelector('.select2-dropdown');
      if (dropdown) dropdown.classList.remove('hidden');
    }
  };

  // 2. Lógica inicial una vez cargado el DOM
  document.addEventListener('DOMContentLoaded', () => {
    console.log("Formulario e interfaz inicializados correctamente.");
  });
  

window.onload = function () {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('fecha_inicio').value = today;
    document.getElementById('honorarios_fecha').value = today;
    document.getElementById('poliza_fecha').value = today;

    // Initialize default select2 values
    selectSelect2Option('customer', mockCustomers[0].id, mockCustomers[0].text);
    selectSelect2Option('advisor', mockAdvisors[0].id, mockAdvisors[0].text);

    calculateDatesAndBalances();
    renderDynamicGuaranteeFields();
    renderExistingCreditsList();
    calculateDisbursementTotals();

    

    // Close select2 dropdowns when clicking outside
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.select2-custom-container')) {
            document.querySelectorAll('.select2-dropdown').forEach(el => el.classList.add('hidden'));
        }
    });
};

// Custom Searchable Dropdown (Select2) Logic
function openSelect2(type) {
    document.querySelectorAll('.select2-dropdown').forEach(el => el.classList.add('hidden'));
    const dropdown = document.getElementById(`${type}_dropdown`);
    dropdown.classList.remove('hidden');
    filterSelect2Options(type);
}

function filterSelect2Options(type) {
    const inputVal = document.getElementById(`${type}_search_input`).value.toLowerCase();
    const dropdown = document.getElementById(`${type}_dropdown`);
    const data = (type === 'customer') ? mockCustomers : mockAdvisors;

    const filtered = data.filter(item => item.text.toLowerCase().includes(inputVal));

    if (filtered.length === 0) {
        dropdown.innerHTML = `<div class="p-3 text-xs text-brandGrayText text-center">No se encontraron resultados</div>`;
        return;
    }

    dropdown.innerHTML = filtered.map(item => `
                <div class="select2-option" onclick="selectSelect2Option('${type}', '${item.id}', '${item.text.replace(/'/g, "\\'")}')">
                    ${item.text}
                </div>
            `).join('');
}

function selectSelect2Option(type, id, text) {
    document.getElementById(`${type}_search_input`).value = text;
    document.getElementById(type === 'customer' ? 'customer_id' : 'asesor_de_credito').value = id;
    document.getElementById(`${type}_dropdown`).classList.add('hidden');
}

function switchTab(tabId) {
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

function toggleGracePeriod() {
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

function calculateDatesAndBalances() {
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

function generatePaymentPlan() {
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const tasaAnual = parseFloat(document.getElementById('tasa_interes').value) || 0;
    const plazo = parseInt(document.getElementById('plazo').value) || 1;
    const formaPago = document.getElementById('forma_de_pago').value;
    const fechaInicioVal = document.getElementById('fecha_inicio').value;
    const plazoGracia = parseInt(document.getElementById('plazo_gracia').value) || 0;

    const tbody = document.getElementById('plan-table-body');
    const tfoot = document.getElementById('plan-table-foot');
    const summaryText = document.getElementById('plan-summary-text');
    tbody.innerHTML = '';

    summaryText.textContent = `Monto: Q ${monto.toFixed(2)} | Tasa: ${tasaAnual}% | Plazo: ${plazo} meses | Método: ${formaPago}`;

    let saldo = monto;
    const tasaMensual = (tasaAnual / 100) / 12;
    let totalCapital = 0;
    let totalInteres = 0;
    let totalCuotas = 0;

    let startDate = fechaInicioVal ? new Date(fechaInicioVal + 'T00:00:00') : new Date();

    const cuotaNivelada = tasaMensual > 0 ? (monto * tasaMensual) / (1 - Math.pow(1 + tasaMensual, -plazo)) : monto / plazo;
    const capitalConstante = monto / plazo;

    for (let i = 1; i <= plazo; i++) {
        let payDate = new Date(startDate);
        payDate.setMonth(payDate.getMonth() + i);
        let fechaStr = payDate.toLocaleDateString('es-GT', { year: 'numeric', month: '2-digit', day: '2-digit' });

        let interes = saldo * tasaMensual;
        let capital = 0;
        let cuota = 0;

        if (formaPago === 'NIVELADA') {
            cuota = cuotaNivelada;
            capital = cuota - interes;
        } else if (formaPago === 'AMORTIZACIÓN A CAPITAL') {
            capital = capitalConstante;
            cuota = capital + interes;
        } else if (formaPago === 'INTERES MENSUAL Y CAPITAL AL VENCIMIENTO') {
            capital = (i === plazo) ? monto : 0;
            cuota = interes + capital;
        } else if (formaPago === 'INTERES Y CAPITAL AL VENCIMIENTO') {
            interes = (i <= plazoGracia) ? interes : (saldo * tasaMensual);
            capital = (i === plazo) ? monto : 0;
            cuota = (i === plazo) ? (monto + (interes * plazo)) : 0;
        }

        if (capital > saldo) capital = saldo;
        let saldoFinal = Math.max(0, saldo - capital);

        totalCapital += capital;
        totalInteres += interes;
        totalCuotas += cuota;

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-brandBgLight/80 transition-colors border-b border-brandGrayBorder/30';
        tr.innerHTML = `
                    <td class="p-3 text-center font-mono text-brandGrayText font-semibold">${i}</td>
                    <td class="p-3 font-medium text-darkCard">${fechaStr}</td>
                    <td class="p-3 text-right font-mono">Q ${saldo.toFixed(2)}</td>
                    <td class="p-3 text-right font-mono text-emerald-600 font-semibold">Q ${capital.toFixed(2)}</td>
                    <td class="p-3 text-right font-mono text-amber-600 font-semibold">Q ${interes.toFixed(2)}</td>
                    <td class="p-3 text-right font-mono font-bold text-brandRedDark">Q ${cuota.toFixed(2)}</td>
                    <td class="p-3 text-right font-mono text-brandGrayText">Q ${saldoFinal.toFixed(2)}</td>
                `;
        tbody.appendChild(tr);

        saldo = saldoFinal;
    }

    tfoot.innerHTML = `
                <tr>
                    <td colspan="3" class="p-3 uppercase">Totales del Plan</td>
                    <td class="p-3 text-right font-mono text-emerald-700">Q ${totalCapital.toFixed(2)}</td>
                    <td class="p-3 text-right font-mono text-amber-700">Q ${totalInteres.toFixed(2)}</td>
                    <td class="p-3 text-right font-mono font-bold text-brandRedDark">Q ${totalCuotas.toFixed(2)}</td>
                    <td class="p-3"></td>
                </tr>
            `;
}

function renderDynamicGuaranteeFields() {
    const tipo = document.getElementById('tipo_garantia').value;
    const container = document.getElementById('dynamic-guarantee-fields');
    container.innerHTML = '';

    let fieldsHTML = '';

    if (tipo === 'HIPOTECA' || tipo === 'DERECHO DE POSESION HIPOTECA') {
        fieldsHTML = `
                    <div><label class="block text-xs text-brandGrayText mb-1">No. Finca</label><input type="text" id="json_finca" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="1234"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Folio</label><input type="text" id="json_folio" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="56"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Libro</label><input type="text" id="json_libro" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="78E"></div>
                    <div class="md:col-span-2"><label class="block text-xs text-brandGrayText mb-1">Dirección del Inmueble</label><input type="text" id="json_direccion" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Ubicación exacta..."></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Área (m²)</label><input type="text" id="json_area" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="250 m²"></div>
                `;
    } else if (tipo === 'FIADOR') {
        fieldsHTML = `
                    <div><label class="block text-xs text-brandGrayText mb-1">Nombre Completo Fiador</label><input type="text" id="json_fiador_nombre" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Nombre completo..."></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">DPI Fiador</label><input type="text" id="json_fiador_dpi" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="CUI / DPI..."></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">NIT</label><input type="text" id="json_fiador_nit" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="NIT..."></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Teléfono</label><input type="text" id="json_fiador_tel" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="5544-3322"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Ingreso Mensual (Q)</label><input type="number" id="json_fiador_ingreso" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="12000.00"></div>
                `;
    } else if (tipo === 'CHEQUE / PAGARE') {
        fieldsHTML = `
                    <div><label class="block text-xs text-brandGrayText mb-1">Banco Emisor</label><input type="text" id="json_banco" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Banco Industrial"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">No. Cheque / Pagaré</label><input type="text" id="json_no_documento" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="CHK-0009812"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Titular de Cuenta</label><input type="text" id="json_titular" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Titular..."></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Fecha Emisión</label><input type="date" id="json_fecha_emision" class="glass-input w-full p-2 rounded-xl text-sm"></div>
                `;
    } else if (tipo === 'VEHICULO') {
        fieldsHTML = `
                    <div><label class="block text-xs text-brandGrayText mb-1">Marca</label><input type="text" id="json_veh_marca" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Toyota"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Línea / Modelo</label><input type="text" id="json_veh_linea" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Hilux"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Año</label><input type="number" id="json_veh_anio" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="2022"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Color</label><input type="text" id="json_veh_color" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Blanco"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Placa</label><input type="text" id="json_veh_placa" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="P-882190"></div>
                `;
    } else if (tipo === 'MOBILIARIA') {
        fieldsHTML = `
                    <div class="md:col-span-2"><label class="block text-xs text-brandGrayText mb-1">Descripción del Bien</label><input type="text" id="json_mob_desc" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="Tractor Agrícola..."></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Marca</label><input type="text" id="json_mob_marca" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="John Deere"></div>
                    <div><label class="block text-xs text-brandGrayText mb-1">Serie</label><input type="text" id="json_mob_serie" class="glass-input w-full p-2 rounded-xl text-sm" placeholder="SN-99120"></div>
                `;
    }

    container.innerHTML = fieldsHTML;
}

function addGuaranteeDetail() {
    const tipo = document.getElementById('tipo_garantia').value;
    const valor = parseFloat(document.getElementById('valor_cobertura').value);

    if (isNaN(valor) || valor <= 0) {
        showToast('Ingrese un valor de cobertura válido superior a Q0.00', 'error');
        return;
    }

    let especificaciones = {};
    if (tipo === 'HIPOTECA' || tipo === 'DERECHO DE POSESION HIPOTECA') {
        especificaciones = {
            finca: document.getElementById('json_finca')?.value || '',
            folio: document.getElementById('json_folio')?.value || '',
            libro: document.getElementById('json_libro')?.value || '',
            direccion: document.getElementById('json_direccion')?.value || '',
            area: document.getElementById('json_area')?.value || ''
        };
    } else if (tipo === 'FIADOR') {
        especificaciones = {
            nombre: document.getElementById('json_fiador_nombre')?.value || '',
            dpi: document.getElementById('json_fiador_dpi')?.value || '',
            nit: document.getElementById('json_fiador_nit')?.value || '',
            telefono: document.getElementById('json_fiador_tel')?.value || '',
            ingreso: document.getElementById('json_fiador_ingreso')?.value || ''
        };
    } else if (tipo === 'CHEQUE / PAGARE') {
        especificaciones = {
            banco: document.getElementById('json_banco')?.value || '',
            no_documento: document.getElementById('json_no_documento')?.value || '',
            titular: document.getElementById('json_titular')?.value || '',
            fecha_emision: document.getElementById('json_fecha_emision')?.value || ''
        };
    } else if (tipo === 'VEHICULO') {
        especificaciones = {
            marca: document.getElementById('json_veh_marca')?.value || '',
            linea: document.getElementById('json_veh_linea')?.value || '',
            anio: document.getElementById('json_veh_anio')?.value || '',
            color: document.getElementById('json_veh_color')?.value || '',
            placa: document.getElementById('json_veh_placa')?.value || ''
        };
    } else if (tipo === 'MOBILIARIA') {
        especificaciones = {
            bien: document.getElementById('json_mob_desc')?.value || '',
            marca: document.getElementById('json_mob_marca')?.value || '',
            serie: document.getElementById('json_mob_serie')?.value || ''
        };
    }

    const item = {
        id: Date.now(),
        tipo_garantia: tipo,
        valor_cobertura: valor,
        especificaciones: especificaciones,
        creation_date: new Date().toISOString()
    };

    guaranteeList.push(item);
    document.getElementById('valor_cobertura').value = '';
    renderDynamicGuaranteeFields();
    updateGuaranteeListDisplay();
    showToast('Detalle de garantía agregado correctamente.', 'success');
}

function removeGuarantee(id) {
    guaranteeList = guaranteeList.filter(g => g.id !== id);
    updateGuaranteeListDisplay();
    showToast('Garantía removida.', 'info');
}

function updateGuaranteeListDisplay() {
    const container = document.getElementById('garantias-list-container');
    const badge = document.getElementById('badge-garantias');
    const totalInput = document.getElementById('suma_total_garantia');
    const totalRegisteredDisplay = document.getElementById('registered-guarantee-total');

    badge.textContent = guaranteeList.length;

    let totalSuma = guaranteeList.reduce((acc, curr) => acc + curr.valor_cobertura, 0);
    totalInput.value = totalSuma.toFixed(2);
    totalRegisteredDisplay.textContent = `Q ${totalSuma.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

    if (guaranteeList.length === 0) {
        container.innerHTML = `
                    <div class="glass-card p-8 text-center text-brandGrayText rounded-xl bg-white/60">
                        <i class="fa-solid fa-folder-open text-3xl mb-2 text-brandRedDark/30"></i>
                        <p>No se han registrado detalles de garantía aún.</p>
                    </div>
                `;
        return;
    }

    container.innerHTML = guaranteeList.map((g, index) => `
                <div class="glass-card p-4 rounded-xl border-l-4 border-l-brandRed bg-white/90 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm">
                    <div class="space-y-1">
                        <div class="flex items-center space-x-2">
                            <span class="px-2 py-0.5 text-xs font-bold bg-brandRedDark text-white rounded">${g.tipo_garantia}</span>
                            <span class="text-xs text-brandGrayText font-semibold">Ítem #${index + 1}</span>
                        </div>
                        <div class="text-xs font-mono text-darkCard bg-brandBgLight p-2 rounded-lg border border-brandGrayBorder/50">
                            <strong class="text-brandRedDark">JSON Specifications:</strong> ${JSON.stringify(g.especificaciones)}
                        </div>
                    </div>
                    <div class="flex items-center space-x-4 w-full md:w-auto justify-between md:justify-end">
                        <div class="text-right">
                            <span class="text-xs text-brandGrayText block">Valor Cobertura</span>
                            <span class="text-base font-bold text-emerald-600 font-mono">Q ${g.valor_cobertura.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
                        </div>
                        <button onclick="removeGuarantee(${g.id})" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                </div>
            `).join('');
}

// Existing Credits Filterable Multi-Select list
function renderExistingCreditsList() {
    filterExistingCreditsList();
}

function filterExistingCreditsList() {
    const query = (document.getElementById('existing_credit_search')?.value || '').toLowerCase();
    const container = document.getElementById('existing-credits-list');

    const filtered = mockExistingCredits.filter(c =>
        c.id.toLowerCase().includes(query) ||
        c.sucursal.toLowerCase().includes(query) ||
        c.titular.toLowerCase().includes(query)
    );

    if (filtered.length === 0) {
        container.innerHTML = `<div class="p-3 text-xs text-brandGrayText text-center">No hay créditos coincidentes</div>`;
        return;
    }

    container.innerHTML = filtered.map(c => `
                <label class="flex items-center justify-between p-2.5 rounded-xl bg-white hover:bg-amber-100/50 border border-brandGrayBorder/60 cursor-pointer text-xs transition-colors">
                    <div class="flex items-center space-x-3">
                        <input type="checkbox" value="${c.total_pendiente}" onchange="calculateDisbursementTotals()" classexisting-credit-chk rounded border-brandGrayBorder text-brandRed focus:ring-brandRed w-4 h-4">
                        <div>
                            <span class="font-bold text-darkCard">${c.id}</span>
                            <span class="text-brandGrayText">(${c.sucursal}) - ${c.titular}</span>
                        </div>
                    </div>
                    <div class="text-right font-mono">
                        <span class="text-amber-700 font-bold">Q ${c.total_pendiente.toFixed(2)}</span>
                        <span class="block text-[10px] text-brandGrayText">Capital: Q${c.saldo_capital.toFixed(2)}</span>
                    </div>
                </label>
            `).join('');
}

function toggleDisbursementMode() {
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

function calculateDisbursementTotals() {
    const montoCredito = parseFloat(document.getElementById('monto').value) || 0;
    const honorarios = parseFloat(document.getElementById('honorarios').value) || 0;
    const poliza = parseFloat(document.getElementById('poliza_seguro').value) || 0;
    const montoDesembolsado = parseFloat(document.getElementById('monto_desembolsado').value) || 0;

    let saldoAnterior = 0;
    document.querySelectorAll('#existing-credits-list input[type="checkbox"]:checked').forEach(chk => {
        saldoAnterior += parseFloat(chk.value) || 0;
    });

    const totalGastos = honorarios + poliza;
    // Formula: monto_total_desembolso = Monto del Credito - (saldo_anterior + poliza + honorarios + monto_desembolsado)
    const montoTotalDesembolsoDiferencia = montoCredito - (saldoAnterior + poliza + honorarios + montoDesembolsado);

    document.getElementById('summary_monto_credito').textContent = `Q ${montoCredito.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    document.getElementById('summary_saldo_anterior').textContent = `Q ${saldoAnterior.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    document.getElementById('summary_honorarios').textContent = `Q ${honorarios.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    document.getElementById('summary_poliza').textContent = `Q ${poliza.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    document.getElementById('summary_monto_desembolsado').textContent = `Q ${montoDesembolsado.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    document.getElementById('summary_total_gastos').textContent = `Q ${totalGastos.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

    const difDisplay = document.getElementById('summary_diferencia');
    const statusMsg = document.getElementById('summary_status_msg');

    difDisplay.textContent = `Q ${montoTotalDesembolsoDiferencia.toLocaleString('es-GT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

    if (Math.abs(montoTotalDesembolsoDiferencia) < 0.01) {
        difDisplay.className = 'text-lg font-bold font-mono text-emerald-600';
        statusMsg.textContent = '✓ El desglose cuadra exactamente con el crédito.';
        statusMsg.className = 'text-[11px] text-emerald-600 font-medium';
    } else if (montoTotalDesembolsoDiferencia > 0) {
        difDisplay.className = 'text-lg font-bold font-mono text-amber-600';
        statusMsg.textContent = `⚠️ Sobrante sin asignar de Q ${montoTotalDesembolsoDiferencia.toFixed(2)}`;
        statusMsg.className = 'text-[11px] text-amber-600 font-medium';
    } else {
        difDisplay.className = 'text-lg font-bold font-mono text-red-600';
        statusMsg.textContent = `❌ Exceso asignado de Q ${Math.abs(montoTotalDesembolsoDiferencia).toFixed(2)}`;
        statusMsg.className = 'text-[11px] text-red-600 font-medium';
    }
}

function openJsonPreviewModal() {
    const customerId = document.getElementById('customer_id').value || null;
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const honorarios = parseFloat(document.getElementById('honorarios').value) || 0;
    const poliza = parseFloat(document.getElementById('poliza_seguro').value) || 0;
    const montoDesembolsado = parseFloat(document.getElementById('monto_desembolsado').value) || 0;

    let saldoAnterior = 0;
    document.querySelectorAll('#existing-credits-list input[type="checkbox"]:checked').forEach(chk => {
        saldoAnterior += parseFloat(chk.value) || 0;
    });

    const payload = {
        credit: {
            proposito: document.getElementById('proposito').value,
            monto: monto,
            plazo: parseInt(document.getElementById('plazo').value),
            tasa_interes: parseFloat(document.getElementById('tasa_interes').value),
            forma_de_pago: document.getElementById('forma_de_pago').value,
            frecuencia_pago: "MENSUAL",
            fecha_inicio: document.getElementById('fecha_inicio').value,
            fecha_vencimiento: document.getElementById('fecha_vencimiento').value,
            tipo_credito: document.getElementById('tipo_credito').value,
            destino_id: null,
            customer_id: customerId,
            saldo_pendiente: monto,
            estados_fechas: "ACTIVO",
            plazo_restante: parseInt(document.getElementById('plazo').value),
            is_paid_off: false,
            estado_aportacion: "PENDIENTE",
            saldo_actual: null,
            sucursal: document.getElementById('sucursal').value,
            asesor_de_credito: document.getElementById('asesor_de_credito').value,
            plazo_gracia: parseInt(document.getElementById('plazo_gracia').value) || 0,
            fecha_finalizacion_gracia: document.getElementById('fecha_finalizacion_gracia').value
        },
        guarantees_header: {
            descripcion: document.getElementById('garantia_descripcion_general').value,
            suma_total: parseFloat(document.getElementById('suma_total_garantia').value) || 0
        },
        guarantees_details: guaranteeList.map(g => ({
            tipo_garantia: g.tipo_garantia,
            especificaciones: g.especificaciones,
            valor_cobertura: g.valor_cobertura
        })),
        disbursement: {
            forma_desembolso: document.getElementById('forma_desembolso').value,
            monto_credito: monto,
            saldo_anterior: saldoAnterior,
            honorarios: honorarios,
            poliza_seguro: poliza,
            monto_desembolsado: montoDesembolsado,
            total_gastos: honorarios + poliza,
            monto_total_desembolso: monto - (saldoAnterior + poliza + honorarios + montoDesembolsado),
            description: document.getElementById('disbursement_description').value
        }
    };

    document.getElementById('json-modal-content').textContent = JSON.stringify(payload, null, 2);
    document.getElementById('json-modal').classList.remove('hidden');
}

function closeJsonPreviewModal() {
    document.getElementById('json-modal').classList.add('hidden');
}

function copyJsonToClipboard() {
    const text = document.getElementById('json-modal-content').textContent;
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast('JSON copiado al portapapeles', 'success');
}

function finalizeRegistration() {
    const customer = document.getElementById('customer_id').value;
    if (!customer) {
        showToast('Seleccione un cliente en el buscador de la pestaña Crédito.', 'error');
        switchTab('credito');
        return;
    }

    openJsonPreviewModal();
    showToast('¡Registro validado! Datos listos para guardado Django.', 'success');
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');

    let bgClass = 'bg-white text-darkCard border-brandGrayBorder';
    let icon = 'fa-circle-info text-sky-600';

    if (type === 'success') {
        bgClass = 'bg-emerald-50 text-emerald-900 border-emerald-300';
        icon = 'fa-circle-check text-emerald-600';
    } else if (type === 'error') {
        bgClass = 'bg-red-50 text-red-900 border-red-300';
        icon = 'fa-triangle-exclamation text-red-600';
    }

    toast.className = `p-4 rounded-xl shadow-xl backdrop-blur-md border flex items-center space-x-3 text-xs font-medium transition-all duration-300 transform translate-y-2 opacity-0 ${bgClass}`;
    toast.innerHTML = `<i class="fa-solid ${icon} text-base"></i><span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
    }, 10);

    setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
