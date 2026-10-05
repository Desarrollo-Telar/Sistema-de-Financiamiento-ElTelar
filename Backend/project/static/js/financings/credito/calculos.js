

window.calculateDatesAndBalances = calculateDatesAndBalances;
window.formatDateToISO = formatDateToISO;

// Función helper para formatear Date a YYYY-MM-DD
function formatDateToISO(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

export function calculateDatesAndBalances() {
    const fechaInicioVal = document.getElementById('fecha_inicio').value;
    const plazoMeses = parseInt(document.getElementById('plazo').value) || 0;
    const plazoGracia = parseInt(document.getElementById('plazo_gracia').value) || 0;

    if (fechaInicioVal) {
        // Asegurar la fecha parseando YYYY-MM-DD
        const [year, month, day] = fechaInicioVal.split('-').map(Number);
        const startDate = new Date(year, month - 1, day);

        // Expiration Date = Start Date + plazo
        const expDate = new Date(startDate);
        expDate.setMonth(expDate.getMonth() + plazoMeses);
        
        // Formato obligatorio para Django: YYYY-MM-DD
        document.getElementById('fecha_vencimiento').value = formatDateToISO(expDate);

        // Grace Date = Start Date + plazo_gracia
        const graciaInput = document.getElementById('fecha_finalizacion_gracia');
        if (plazoGracia > 0 && !document.getElementById('plazo_gracia').disabled) {
            const graceDate = new Date(startDate);
            graceDate.setMonth(graceDate.getMonth() + plazoGracia);
            graciaInput.value = formatDateToISO(graceDate);
        } else {
            // Enviar cadena vacía para que Django interprete null/blank correctamente
            graciaInput.value = '';
        }
    }

    calculateDisbursementTotals();
}

window.calculateDisbursementTotals = calculateDisbursementTotals;

export function calculateDisbursementTotals() {

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

    // Se recorren todos los checkboxes seleccionados de la lista o área de créditos
    document
        .querySelectorAll(
            '#existing-credits-list .existing-credit-chk:checked, .existing-credit-chk:checked'
        )
        .forEach(chk => {

            // Se obtiene la propiedad saldoActual del dataset
            const saldoPendiente =
                parseFloat(chk.dataset.saldoActual) || 0;

            saldoAnterior += saldoPendiente;
        });


    // ==========================================================
    // TOTAL DE GASTOS
    // ==========================================================

    const totalGastos =
        honorarios + poliza + montoDesembolsado + saldoAnterior;


    // ==========================================================
    // DIFERENCIA DEL DESEMBOLSO
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

    const elemMontoCredito = document.getElementById('summary_monto_credito');
    if (elemMontoCredito) elemMontoCredito.textContent = formatoMoneda(montoCredito);

    const elemSaldoAnterior = document.getElementById('summary_saldo_anterior');
    if (elemSaldoAnterior) elemSaldoAnterior.textContent = formatoMoneda(saldoAnterior);

    const elemHonorarios = document.getElementById('summary_honorarios');
    if (elemHonorarios) elemHonorarios.textContent = formatoMoneda(honorarios);

    const elemPoliza = document.getElementById('summary_poliza');
    if (elemPoliza) elemPoliza.textContent = formatoMoneda(poliza);

    const elemMontoDesembolsado = document.getElementById('summary_monto_desembolsado');
    if (elemMontoDesembolsado) elemMontoDesembolsado.textContent = formatoMoneda(montoDesembolsado);

    const elemTotalGastos = document.getElementById('summary_total_gastos');
    if (elemTotalGastos) elemTotalGastos.textContent = formatoMoneda(totalGastos);


    // ==========================================================
    // DIFERENCIA
    // ==========================================================

    const difDisplay = document.getElementById('summary_diferencia');
    const statusMsg = document.getElementById('summary_status_msg');

    if (difDisplay) {
        difDisplay.textContent = formatoMoneda(montoTotalDesembolsoDiferencia);
    }


    // ==========================================================
    // ESTADO DEL DESGLOSE
    // ==========================================================

    if (difDisplay && statusMsg) {

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
    }
}