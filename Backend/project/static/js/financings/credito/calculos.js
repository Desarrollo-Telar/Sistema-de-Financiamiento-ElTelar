

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


    calculateDisbursementTotals();
}


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