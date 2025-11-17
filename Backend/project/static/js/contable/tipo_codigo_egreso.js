import { ocultar, mostrar } from './ocultar_mostrar.js';
import { oculto } from './ocultar_todo.js';

export function tipo_codigo(input_id_codigo_egreso, seleccionado) {
    console.log(input_id_codigo_egreso);

    switch (input_id_codigo_egreso) {
        case 'SALARIOS':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));

            mostrar(document.getElementById('id_nombre'));
            mostrar(document.querySelector('label[for="id_nombre"]'));
            // Obtener el input
            const inputNombre = document.getElementById('id_nombre');

            // Crear el nuevo select
            const selectNombre = document.createElement('select');
            selectNombre.id = inputNombre.id; // Mantiene el mismo ID
            selectNombre.name = inputNombre.name; // Mantiene el mismo name
            selectNombre.className = inputNombre.className; // Mantiene las mismas clases
            selectNombre.style = inputNombre.style; // Mantiene los estilos en línea

            // Opciones del select
            const opciones = ['EDGAR ARMANDO ALVARADO ', 'LUISA FERNANDA CHEN PACAY', 'ELIZABETH ANDREA ESPERANZA TOT CANAHUI', 'GRECIA MAYARI RODRIGUEZ ROQUEL', 'JALINNE ANAGALY BERRÍOS DE LA CRUZ']; // Modifica según sea necesario
            opciones.forEach(opcion => {
                const optionElement = document.createElement('option');
                optionElement.value = opcion;
                optionElement.textContent = opcion;
                selectNombre.appendChild(optionElement);
            });

            // Reemplazar el input con el select
            inputNombre.replaceWith(selectNombre);


            mostrar(document.getElementById('id_pago_correspondiente'));
            mostrar(document.querySelector('label[for="id_pago_correspondiente"]'));
            // Obtener el input
            const id_pago_correspondiente = document.getElementById('id_pago_correspondiente');

            // Crear el nuevo select
            const selectid_pago_correspondiente = document.createElement('select');
            selectid_pago_correspondiente.id = id_pago_correspondiente.id; // Mantiene el mismo ID
            selectid_pago_correspondiente.name = id_pago_correspondiente.name; // Mantiene el mismo name
            selectid_pago_correspondiente.className = id_pago_correspondiente.className; // Mantiene las mismas clases
            selectid_pago_correspondiente.style = id_pago_correspondiente.style; // Mantiene los estilos en línea

            // Opciones del select
            const opciones_id_pago_correspondiente = [
                'PRIMERA QUINCENA', 'SEGUNDA QUINCENA',
                'AGUINALDO ', 'BONO 14 ',
                'HORAS EXTRA', 'OTRAS BONIFICACIONES ',
                'OTROS PAGOS'
            ]; // Modifica según sea necesario
            opciones_id_pago_correspondiente.forEach(opcion => {
                const optionElement = document.createElement('option');
                optionElement.value = opcion;
                optionElement.textContent = opcion;
                selectid_pago_correspondiente.appendChild(optionElement);
            });

            // Reemplazar el input con el select
            id_pago_correspondiente.replaceWith(selectid_pago_correspondiente);


            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));

            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));


            break;
        case 'ALQUILER':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));





            break;

        case 'GASTOS POR DESEMBOLSOS':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));

            mostrar(document.getElementById('id_tipo_gasto'));
            mostrar(document.querySelector('label[for="id_tipo_gasto"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));
            
            // Obtener el input
            const id_tipo_gasto = document.getElementById('id_tipo_gasto');

            // Crear el nuevo select
            const select_id_tipo_gasto = document.createElement('select');
            select_id_tipo_gasto.id = id_tipo_gasto.id; // Mantiene el mismo ID
            select_id_tipo_gasto.name = id_tipo_gasto.name; // Mantiene el mismo name
            select_id_tipo_gasto.className = id_tipo_gasto.className; // Mantiene las mismas clases
            select_id_tipo_gasto.style = id_tipo_gasto.style; // Mantiene los estilos en línea

            // Opciones del select
            const opciones_id_tipo_gasto = [
                'PAGO DE HONORARIOS POR DESEMBOLSO ', 'CERTIFICACIONES',
                'OTROS DOCUMENTOS'
            ]; // Modifica según sea necesario
            opciones_id_tipo_gasto.forEach(opcion => {
                const optionElement = document.createElement('option');
                optionElement.value = opcion;
                optionElement.textContent = opcion;
                select_id_tipo_gasto.appendChild(optionElement);
            });

            // Reemplazar el input con el select
            id_tipo_gasto.replaceWith(select_id_tipo_gasto);

            break;

        case 'OTROS GASTOS GENERALES':
            if (seleccionado){
                oculto();

            }
            console.log(seleccionado)
            
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));

            mostrar(document.getElementById('id_pago_correspondiente'));
            mostrar(document.querySelector('label[for="id_pago_correspondiente"]'));
            document.querySelector('label[for="id_pago_correspondiente"]').textContent = 'Pago Realizado A:';

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));

            break;
        case 'COMBUSTIBLES':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_fecha_doc_fiscal'));
            mostrar(document.querySelector('label[for="id_fecha_doc_fiscal"]'));

            mostrar(document.getElementById('id_numero_doc'));
            mostrar(document.querySelector('label[for="id_numero_doc"]'));

            mostrar(document.getElementById('id_nit'));
            mostrar(document.querySelector('label[for="id_nit"]'));

            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            break;
        case 'PAPELERIA Y UTILES':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_fecha_doc_fiscal'));
            mostrar(document.querySelector('label[for="id_fecha_doc_fiscal"]'));

            mostrar(document.getElementById('id_numero_doc'));
            mostrar(document.querySelector('label[for="id_numero_doc"]'));

            mostrar(document.getElementById('id_nit'));
            mostrar(document.querySelector('label[for="id_nit"]'));

            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            break;
        case 'ALIMENTACIÓN':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_fecha_doc_fiscal'));
            mostrar(document.querySelector('label[for="id_fecha_doc_fiscal"]'));

            mostrar(document.getElementById('id_numero_doc'));
            mostrar(document.querySelector('label[for="id_numero_doc"]'));

            mostrar(document.getElementById('id_nit'));
            mostrar(document.querySelector('label[for="id_nit"]'));

            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            break;

        case 'GASTOS DE MANTENIMIENTO':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_fecha_doc_fiscal'));
            mostrar(document.querySelector('label[for="id_fecha_doc_fiscal"]'));

            mostrar(document.getElementById('id_numero_doc'));
            mostrar(document.querySelector('label[for="id_numero_doc"]'));

            mostrar(document.getElementById('id_nit'));
            mostrar(document.querySelector('label[for="id_nit"]'));

            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            break;
        case 'EQUIPO DE COMPUTACIÓN':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_fecha_doc_fiscal'));
            mostrar(document.querySelector('label[for="id_fecha_doc_fiscal"]'));

            mostrar(document.getElementById('id_numero_doc'));
            mostrar(document.querySelector('label[for="id_numero_doc"]'));

            mostrar(document.getElementById('id_nit'));
            mostrar(document.querySelector('label[for="id_nit"]'));

            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            break;
        case 'SERVICIOS TERCEROS':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_fecha_doc_fiscal'));
            mostrar(document.querySelector('label[for="id_fecha_doc_fiscal"]'));

            mostrar(document.getElementById('id_numero_doc'));
            mostrar(document.querySelector('label[for="id_numero_doc"]'));

            mostrar(document.getElementById('id_nit'));
            mostrar(document.querySelector('label[for="id_nit"]'));

            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            break;
        case 'COMUNICACIONES':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));
            mostrar(document.getElementById('id_fecha_doc_fiscal'));
            mostrar(document.querySelector('label[for="id_fecha_doc_fiscal"]'));

            mostrar(document.getElementById('id_numero_doc'));
            mostrar(document.querySelector('label[for="id_numero_doc"]'));

            mostrar(document.getElementById('id_nit'));
            mostrar(document.querySelector('label[for="id_nit"]'));

            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));

            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));

            mostrar(document.getElementById('id_monto_doc'));
            mostrar(document.querySelector('label[for="id_monto_doc"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            break;
        case 'PAGO DE IMPUESTOS':
            oculto();
            mostrar(document.getElementById('btn_registro'));
            mostrar(document.getElementById('id_fecha'));
            mostrar(document.querySelector('label[for="id_fecha"]'));

            mostrar(document.getElementById('id_tipo_impuesto'));
            mostrar(document.querySelector('label[for="id_tipo_impuesto"]'));
            // Obtener el input
            const id_tipo_impuesto = document.getElementById('id_tipo_impuesto');

            // Crear el nuevo select
            const select_id_tipo_impuesto = document.createElement('select');
            select_id_tipo_impuesto.id = id_tipo_impuesto.id; // Mantiene el mismo ID
            select_id_tipo_impuesto.name = id_tipo_impuesto.name; // Mantiene el mismo name
            select_id_tipo_impuesto.className = id_tipo_impuesto.className; // Mantiene las mismas clases
            select_id_tipo_impuesto.style = id_tipo_impuesto.style; // Mantiene los estilos en línea

            // Opciones del select
            const opciones_id_tipo_impuesto = [
                'IVA', 'ISR', 'ISO', 'OTROS IMPUETOS TASAS Y ABITRIOS'
                
            ]; // Modifica según sea necesario
            opciones_id_tipo_impuesto.forEach(opcion => {
                const optionElement = document.createElement('option');
                optionElement.value = opcion;
                optionElement.textContent = opcion;
                select_id_tipo_impuesto.appendChild(optionElement);
            });

            // Reemplazar el input con el select
            id_tipo_impuesto.replaceWith(select_id_tipo_impuesto);
            mostrar(document.getElementById('id_monto'));
            mostrar(document.querySelector('label[for="id_monto"]'));
            mostrar(document.getElementById('id_boleta'));
            mostrar(document.querySelector('label[for="id_boleta"]'));
            mostrar(document.getElementById('id_documento'));
            mostrar(document.querySelector('label[for="id_documento"]'));
            document.querySelector('label[for="id_documento"]').textContent = 'Foto Boleta De Pago:';
            mostrar(document.getElementById('id_observaciones'));
            mostrar(document.querySelector('label[for="id_observaciones"]'));
            mostrar(document.getElementById('id_numero_referencia'));
            mostrar(document.querySelector('label[for="id_numero_referencia"]'));

            break;
        default:
            oculto();

            break;
    }

}