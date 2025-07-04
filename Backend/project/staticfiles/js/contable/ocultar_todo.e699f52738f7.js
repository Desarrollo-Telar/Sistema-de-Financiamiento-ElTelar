import { ocultar } from './ocultar_mostrar.js'
const input_fecha = document.getElementById('id_fecha') || NaN;
const label_fecha = document.querySelector('label[for="id_fecha"]') || NaN;

const input_id_fecha_doc_fiscal = document.getElementById('id_fecha_doc_fiscal') || NaN;
const label_fecha_doc_fiscal = document.querySelector('label[for="id_fecha_doc_fiscal"]') || NaN;

const input_id_numero_doc = document.getElementById('id_numero_doc') || NaN;
const label_id_numero_doc = document.querySelector('label[for="id_numero_doc"]') || NaN;

const input_id_nit = document.getElementById('id_nit') || NaN;
const label_id_nit = document.querySelector('label[for="id_nit"]') || NaN;

const input_id_monto = document.getElementById('id_monto') || NaN;
const label_id_monto = document.querySelector('label[for="id_monto"]') || NaN;

const input_id_monto_doc = document.getElementById('id_monto_doc') || NaN;
const label_id_monto_doc = document.querySelector('label[for="id_monto_doc"]') || NaN;

const input_id_numero_referencia = document.getElementById('id_numero_referencia') || NaN;
const label_id_numero_referencia = document.querySelector('label[for="id_numero_referencia"]') || NaN;
const input_id_descripcion = document.getElementById('id_descripcion') || NaN;
const label_id_descripcion = document.querySelector('label[for="id_descripcion"]') || NaN;

const input_id_observaciones = document.getElementById('id_observaciones') || NaN;
const label_id_observaciones = document.querySelector('label[for="id_observaciones"]') || NaN;

const input_id_boleta = document.getElementById('id_boleta') || NaN;
const label_id_boleta = document.querySelector('label[for="id_boleta"]') || NaN;
//
const input_id_documento = document.getElementById('id_documento') || NaN;
const label_id_documento = document.querySelector('label[for="id_documento"]') || NaN;

const input_id_nombre = document.getElementById('id_nombre');
const label_id_nombre = document.querySelector('label[for="id_nombre"]');

const input_id_pago_correspondiente = document.getElementById('id_pago_correspondiente');
const label_id_pago_correspondiente = document.querySelector('label[for="id_pago_correspondiente"]');

const input_id_tipo_impuesto = document.getElementById('id_tipo_impuesto') || NaN;
const label_id_tipo_impuesto = document.querySelector('label[for="id_tipo_impuesto"]') || NaN;

export function oculto() {
    
    document.querySelector('label[for="id_pago_correspondiente"]').textContent = 'Pago Correspondiente:';
    document.querySelector('label[for="id_documento"]').textContent = 'Documento:';
    // Obtener el select
    const selectNombre = document.getElementById('id_nombre');

    // Crear el nuevo input
    const inputNombre = document.createElement('input');
    inputNombre.id = selectNombre.id; // Mantiene el mismo ID
    inputNombre.name = selectNombre.name; // Mantiene el mismo name
    inputNombre.className = selectNombre.className; // Mantiene las mismas clases
    inputNombre.style = selectNombre.style; // Mantiene los estilos en línea
    inputNombre.type = 'text'; // Define el tipo como 'text'
    inputNombre.value = ''; // Asigna el valor seleccionado en el select

    // Reemplazar el select con el input
    selectNombre.replaceWith(inputNombre);

    // Obtener el select
    const selectPagoCorrespondinte = document.getElementById('id_pago_correspondiente');

    // Crear el nuevo input
    const inputPagoCorrespondiente = document.createElement('input');
    inputPagoCorrespondiente.id = selectPagoCorrespondinte.id; // Mantiene el mismo ID
    inputPagoCorrespondiente.name = selectPagoCorrespondinte.name; // Mantiene el mismo name
    inputPagoCorrespondiente.className = selectPagoCorrespondinte.className; // Mantiene las mismas clases
    inputPagoCorrespondiente.style = selectPagoCorrespondinte.style; // Mantiene los estilos en línea
    inputPagoCorrespondiente.type = 'text'; // Define el tipo como 'text'
    inputPagoCorrespondiente.value = ''; // Asigna el valor seleccionado en el select

    // Reemplazar el select con el input
    selectPagoCorrespondinte.replaceWith(inputPagoCorrespondiente);

    // Obtener el select
    const selectTipoGasto = document.getElementById('id_tipo_gasto');

    // Crear el nuevo input
    const inputTipoGasto = document.createElement('input');
    inputTipoGasto.id = selectTipoGasto.id; // Mantiene el mismo ID
    inputTipoGasto.name = selectTipoGasto.name; // Mantiene el mismo name
    inputTipoGasto.className = selectTipoGasto.className; // Mantiene las mismas clases
    inputTipoGasto.style = selectTipoGasto.style; // Mantiene los estilos en línea
    inputTipoGasto.type = 'text'; // Define el tipo como 'text'
    inputTipoGasto.value = ''; // Asigna el valor seleccionado en el select

    // Reemplazar el select con el input
    selectTipoGasto.replaceWith(inputTipoGasto);

    ocultar(document.getElementById('id_nombre'));
    ocultar(document.getElementById('id_pago_correspondiente'));
    ocultar(document.getElementById('id_tipo_gasto'));
    ocultar(document.querySelector('label[for="id_tipo_gasto"]'));
    ocultar(document.getElementById('id_tipo_impuesto'));
    ocultar(document.getElementById('btn_registro'));

    ocultar(input_fecha);
    ocultar(label_fecha);

    ocultar(input_id_fecha_doc_fiscal);
    ocultar(label_fecha_doc_fiscal);

    ocultar(input_id_numero_doc);
    ocultar(label_id_numero_doc);

    ocultar(input_id_nit);
    ocultar(label_id_nit);

    ocultar(input_id_monto);
    ocultar(label_id_monto);

    ocultar(input_id_monto_doc);
    ocultar(label_id_monto_doc);

    ocultar(input_id_numero_referencia);
    ocultar(label_id_numero_referencia);

    ocultar(input_id_descripcion);
    ocultar(label_id_descripcion);

    ocultar(input_id_observaciones);
    ocultar(label_id_observaciones);

    ocultar(input_id_boleta);
    ocultar(label_id_boleta);

    ocultar(input_id_documento);
    ocultar(label_id_documento);

    ocultar(input_id_nombre);
    ocultar(label_id_nombre);

    ocultar(input_id_pago_correspondiente);
    ocultar(label_id_pago_correspondiente);

    ocultar(input_id_tipo_impuesto);
    ocultar(label_id_tipo_impuesto);

}