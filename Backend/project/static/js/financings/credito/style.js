
import {calculateDatesAndBalances, calculateDisbursementTotals} from './calculos.js'

// Seleccionar opción

let activeTab = 'credito';

let existingCreditsSearchTimeout = null;

let listado_formas = ['APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE', 'REESTRUCTURACIÓN DE CRÉDITO VIGENTE'];

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

    if (listado_formas.includes(mode)) {
        panel.classList.remove('hidden');
    } else {
        panel.classList.add('hidden');
        document.querySelectorAll('.existing-credit-chk').forEach(chk => chk.checked = false);
    }
    calculateDisbursementTotals();
}


export function showToast(message, type = 'info') {
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




