// Función para limpiar campos del formulario
export function clearFields() {
    document.getElementById('noEscritura').value = '';
    document.getElementById('notario').value = '';
    document.getElementById('finca').value = '';
    document.getElementById('folio').value = '';
    document.getElementById('libro').value = '';
    document.getElementById('area').value = '';
    document.getElementById('ubicacion').value = '';
    document.getElementById('descripcion').value = '';
    document.getElementById('valor_comercial').value = '';
    document.getElementById('titular').value = '';
    document.getElementById('estatus').value = '';
    document.getElementById('noContratoArrendamiento').value = '';
    //document.getElementById('avaluoBien').value = '';
    //document.getElementById('docDigitalSoporte').value = '';
    document.getElementById('valor_cobertura').value = '';
    document.getElementById('noCheque').value = '';
    document.getElementById('nombreCuenta').value= '';
    document.getElementById('banco').value= '';
    document.getElementById('cheque_girado_a').value= '';
    document.getElementById('monto_cheque').value= '';
    document.getElementById('cheque').value= '';
}