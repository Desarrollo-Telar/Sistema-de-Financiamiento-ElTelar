
import {calculateDatesAndBalances, calculateDisbursementTotals} from './calculos.js'

// Seleccionar opción

let activeTab = 'credito';

let existingCreditsSearchTimeout = null;

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







