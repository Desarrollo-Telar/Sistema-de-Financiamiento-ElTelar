// Función para obtener valor numérico de un campo por ID
const obtenerValorNumerico = (id) => parseFloat(document.getElementById(id)?.value) || 0;

const campos = ['monto', 'poliza_seguro', 'honorarios', 'credito_saldo_capital_vigente', 'monto_desembolsado'];
campos.forEach(id => {
    const elemento = document.getElementById(id);
    if (elemento) {
        elemento.addEventListener('input', actualizarTotalDepositar);
    }
});

export function actualizarTotalDepositar() {
    
    const monto = obtenerValorNumerico('monto'); // Monto del credito
    const poliza_seguro = obtenerValorNumerico('poliza_seguro'); // Poliza de Seguro de desembolso
    const honorarios = obtenerValorNumerico('honorarios'); // Honorarios de desembolso
    const saldo_anterior = obtenerValorNumerico('credito_saldo_capital_vigente'); // Saldo anterior del otro credito vigente
    const monto_desembolsado = obtenerValorNumerico('monto_desembolsado');
    let gastos = parseFloat(poliza_seguro) + parseFloat(honorarios) + parseFloat(saldo_anterior) + parseFloat(monto_desembolsado);
    document.getElementById('total_gastos').value = parseFloat(gastos).toFixed(2);
    
    let total_depositars = parseFloat(monto) - parseFloat(gastos);
    document.getElementById('total_depositar').value = parseFloat(total_depositars).toFixed(2);
}