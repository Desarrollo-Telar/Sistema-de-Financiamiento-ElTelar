import {urls_p} from '../../API/urls_api.js'

import {registrar_credito} from '../../API/credito/crear_credito.js'
import {actualizar_credito} from '../../API/credito/actualizar.js'

import { registrar_desembolso } from '../../API/desembolsos/crear_desembolsos.js'

import {registrar_pago} from '../../API/pagos/crear_pago.js'

import { suma_total, lista_garantia, list_form_data} from './garantia.js'

import {get_credit} from '../../API/credito/obtener_credito.js'

function get_tasaInteres() {
    const tasa = document.getElementById('tasa_interes').value;

    return tasa > 1 ? (tasa / 12)/100 : tasa/12;
}
export async function guardar_credito(monto){
    let formData = new FormData();
    formData.append('proposito',document.getElementById('proposito').value);
    formData.append('monto',monto);
    formData.append('plazo',document.getElementById('plazo').value);
    formData.append('tasa_interes',get_tasaInteres());
    formData.append('forma_de_pago',document.getElementById('forma_de_pago').value);
    formData.append('frecuencia_pago','MENSUAL');
    formData.append('fecha_inicio',document.getElementById('fecha_inicio').value);
    formData.append('fecha_vencimiento',document.getElementById('fecha_vencimiento').value);
    formData.append('tipo_credito',document.getElementById('tipo_credito').value);
    formData.append('customer_id',document.getElementById('customer_id').value);
    formData.append('saldo_pendiente',document.getElementById('monto').value);
    formData.append('estados_fechas',true);
    //formData.append('plazo_restante',document.getElementById('plazo_restante_c').value);
    formData.append('is_paid_off',false);
    formData.append('sucursal',document.getElementById('sucursal_id').value);
    formData.append('asesor_de_credito', document.getElementById('asesor_id').value);
    //formData.append('estado_aportacion',NaN);
    return await registrar_credito(formData);
}

export async function guardar_desembolso(credit_id, forma_desembolso, credito_cancelado=NaN) {
    let formData = new FormData();
    let descripcion = document.getElementById('description').value;

    if (forma_desembolso == 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE'){
        credito_cancelado = await get_credit(credito_cancelado);
        descripcion = `${descripcion}\nSE AMPLIO DEL CREDITO: ${credito_cancelado.codigo_credito}`;

    }

    formData.append('credit_id', credit_id);
    formData.append('forma_desembolso', forma_desembolso);
    formData.append('monto_credito', document.getElementById('monto').value);
    formData.append('saldo_anterior', document.getElementById('credito_saldo_capital_vigente').value||0);
    formData.append('honorarios', document.getElementById('honorarios').value||0);
    formData.append('poliza_seguro', document.getElementById('poliza_seguro').value||0);
    formData.append('monto_desembolsado', document.getElementById('monto_desembolsado').value||0);
    formData.append('monto_total_desembolso', document.getElementById('total_depositar').value||0);
    formData.append('total_gastos', document.getElementById('total_gastos').value||0);
    formData.append('description', descripcion);


    return await registrar_desembolso(formData);
    
}

export async function registroGarantia(credito_id) {
    try {
        let json = {
            suma_total: suma_total,
            credit_id: credito_id,
            descripcion:'REGISTRO DE GARANTIA',
        };

        console.log(json);

        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) {
            throw new Error('CSRF token not found');
        }
        const csrfToken = csrfTokenElement.getAttribute('content');

        const response = await fetch(urls_p.api_url_garantia, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(json)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        const detalle = await registrarDetalle(data.id);
        console.log(detalle);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

export async function guardar_boleta_desembolso(credit, disbursement, monto,numero_referencia,fecha_emision,descripcion,boleta) {
    let formData = new FormData();
    formData.append('credit', credit);
    formData.append('disbursement', disbursement);
    formData.append('monto', monto);
    formData.append('numero_referencia', numero_referencia);
    formData.append('fecha_emision', fecha_emision);
    formData.append('descripcion', descripcion);
    formData.append('boleta', boleta);
    formData.append('tipo_pago', 'DESEMBOLSO');
    //formData.append('cliente',document.getElementById('cliente').value);
    return await registrar_pago(formData);
    
}

export async function registrarDetalle(garantia_id) {
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const resultados = [];

        for (let element of lista_garantia) {
            let js = {
                garantia_id: garantia_id,
                tipo_garantia: element['tipo_garantia'],
                valor_cobertura: element['valor_cobertura'],
                especificaciones: element['especificacion'],
            };

            console.log(`DETALLE DE GARANTIA ${JSON.stringify(js)}`);

            const response = await fetch(urls_p.api_url_detalle_garantia, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(js)
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.status}`);
            }

            const data = await response.json();
            resultados.push(data);
        }

        return resultados;  // Devolver todas las respuestas al final

    } catch (error) {
        console.error('Error en el envío de detalles:', error);
        throw error;
    }
}
