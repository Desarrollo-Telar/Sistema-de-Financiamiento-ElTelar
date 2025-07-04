import { urls_p } from '../urls_api.js';
import { registrar_pago } from '../pagos/crear_pago.js';
import { actualizar_credito } from '../credito/actualizar.js';
import {get_ultima_cuota} from '../credito/obtener_ultima_cuota.js'
import {calculo_interes} from '../credito/calculos.js'
import {actualizacion_cuota} from '../credito/actualizar_cuota.js'
import { alerta_m } from '../../alertas/alertas.js';

async function registrar_boleta(tipo_pago, desembolso_id, monto, referencia, fecha, boleta, descripcion) {
    const form_data = new FormData();
    form_data.append('disbursement', desembolso_id);
    form_data.append('tipo_pago', tipo_pago);
    form_data.append('monto', monto);
    form_data.append('numero_referencia', referencia);
    form_data.append('fecha_emision', fecha);
    //form_data.append('boleta', boleta);
    form_data.append('descripcion', descripcion);
    return await registrar_pago(form_data);
}

export async function registrar_desembolso(formData) {
    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
    if (!csrfTokenElement) {
        throw new Error('CSRF token not found');
    }
    const csrfToken = csrfTokenElement.getAttribute('content');

    try {
        // Validar parámetros
        if (!formData) {
            throw new Error('FormData no proporcionados.');
        }

        // Realizar solicitud PATCH
        const response = await axios({
            method: 'post',
            url: urls_p.api_url_desembolso,
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrfToken
            },
            data: formData
        });

        console.log('Registro de Desembolso:', response.data);
        return response.data; // Retornar datos de la respuesta

    } catch (error) {
        if (error.response) {
            console.error('Error en la respuesta del servidor:', error.response.data);
            console.error('Código de estado:', error.response.status);
        } else if (error.request) {
            console.error('Error en la solicitud (no hubo respuesta):', error.request);
        } else {
            console.error('Error:', error.message);
        }
        throw error; // Re-lanzar el error para manejo externo si es necesario
    }
}

document.getElementById('desembolso').addEventListener('submit', async function (event) {
    event.preventDefault();
    try {
        let total_desembolso = parseFloat(document.getElementById('total_depositar').value || 0);
        const credit_id = document.getElementById('credit_id').value;
        const valor_seleccionado = document.getElementById('forma_desembolso').value;

        // Crear FormData base
        const formData = new FormData();
        formData.append('forma_desembolso', valor_seleccionado);
        formData.append('monto_credito', parseFloat(document.getElementById('monto_credito').value));

        if (valor_seleccionado === 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE') {
            const monto_credito_agregar = parseFloat(document.getElementById('monto_credito_agregar').value || 0);
            formData.append('monto_credito_agregar', monto_credito_agregar);
            const saldo_pendiente_credito = parseFloat(document.getElementById('saldo_pendiente_credito').value || 0);
            const plazo_restante = parseInt(document.getElementById('plazo_restante').value || 0);
            const plazo_credito = parseInt(document.getElementById('plazo_credito').value);
            const plazo_credito_restante = parseInt(document.getElementById('plazo_credito_restante').value);
            
            console.log(saldo_pendiente_credito);
            console.log(monto_credito_agregar);
            const saldo_pe_a = (saldo_pendiente_credito + monto_credito_agregar).toFixed(2)
            
            // Actualizar crédito
            const form_data_credito = new FormData();
            const monto_credito = parseFloat(document.getElementById('monto_credito').value);
            const monto_ap = (monto_credito + monto_credito_agregar).toFixed(2)
            form_data_credito.append('monto', monto_ap);
            form_data_credito.append('saldo_pendiente', saldo_pe_a);
            form_data_credito.append('plazo', plazo_credito + plazo_restante);
            form_data_credito.append('plazo_restante', plazo_credito_restante + plazo_restante);
            form_data_credito.append('estados_fechas', true);
            

            // Calcular el nuevo interes para la cuota
            const tasa_interes_credito = document.getElementById('tasa_interes_credito').value;
            console.log(tasa_interes_credito);
            console.log(saldo_pe_a);
            const calcular_interes = calculo_interes(saldo_pe_a,tasa_interes_credito);

            // Actualizar Cuota
            // Primero Obtner la Cuota
            const ultima_cuota_vigente = await get_ultima_cuota(credit_id);
            const cuota_interes_acumulado = parseFloat(ultima_cuota_vigente.interes_acumulado_generado || 0).toFixed(2);
            const cuota_interes_pagado = parseFloat(ultima_cuota_vigente.interes_pagado || 0).toFixed(2);
           
            const interes_nuevo =  (parseFloat(cuota_interes_acumulado||0) + parseFloat(calcular_interes)) - parseFloat(cuota_interes_pagado||0)
            console.log(interes_nuevo);
            console.log(calcular_interes);

            const form_data_cuota = new FormData();
            form_data_cuota.append('interest', parseFloat(interes_nuevo).toFixed(2));
            form_data_cuota.append('interes_generado', parseFloat(calcular_interes).toFixed(2));

            const saldo_actual = saldo_pe_a + interes_nuevo + parseFloat(ultima_cuota_vigente.mora||0);
            
            form_data_credito.append('saldo_actual', parseFloat(saldo_actual).toFixed(2));
            
            await actualizar_credito(credit_id, form_data_credito);
            await actualizacion_cuota(ultima_cuota_vigente.id,form_data_cuota)



        } else if (valor_seleccionado === 'CANCELACIÓN DE CRÉDITO VIGENTE') {
            formData.append('monto_credito_cancelar', parseFloat(document.getElementById('monto_credito_cancelar').value || 0));
            total_desembolso = 0;

            // Marcar crédito como pagado
            const form_data_creditos = new FormData();
            form_data_creditos.append('is_paid_off', true);
            form_data_creditos.append('saldo_pendiente', 0);
            form_data_creditos.append('estados_fechas', true);
            form_data_creditos.append('estado_aportacion', true);
            form_data_creditos.append('saldo_actual', 0);
            await actualizar_credito(credit_id, form_data_creditos);
        }

        formData.append('saldo_anterior', parseFloat(document.getElementById('saldo_anterior').value));
        formData.append('honorarios', parseFloat(document.getElementById('honorarios').value || 0));
        formData.append('poliza_seguro', parseFloat(document.getElementById('poliza_seguro').value || 0));
        formData.append('monto_total_desembolso', total_desembolso);
        formData.append('credit_id', credit_id);

        const desembolso = await registrar_desembolso(formData);

        // Registrar pagos relacionados
        const honorarios = parseFloat(document.getElementById('honorarios').value || 0);
        const poliza = parseFloat(document.getElementById('poliza_seguro').value || 0);
        const registrar_pago_boleta = async (tipo, monto, referencia, fecha, boleta, descripcion) => {
            console.log('esperar...');
            await registrar_boleta(tipo, desembolso.id, monto, referencia, fecha, boleta, descripcion);
        };

        if (honorarios > 0) {
            const boleta_h = document.getElementById('boleta_honorarios');
            const boleta_h_f = boleta_h.value;
            await registrar_pago_boleta('DESEMBOLSO', honorarios, 
                document.getElementById('numero_referencia_honorarios').value,
                document.getElementById('fecha_emision_honorarios').value,
                
                boleta_h_f,
                document.getElementById('descripcion_honorarios').value);
        }

        if (poliza > 0) {
            const boleta_p = document.getElementById('boleta_poliza');
            const boleta_p_f = boleta_p.value;
            await registrar_pago_boleta('DESEMBOLSO', poliza, 
                document.getElementById('numero_referencia_poliza').value,
                document.getElementById('fecha_emision_poliza').value,
                boleta_p_f,
                document.getElementById('descripcion_poliza').value);
        }

        if (total_desembolso > 0) {
            const boleta_t = document.getElementById('boleta_total');
            const boleta_t_f = boleta_t.value;

            await registrar_pago_boleta('DESEMBOLSO', total_desembolso, 
                document.getElementById('numero_referencia_total').value,
                document.getElementById('fecha_emision_total').value,
                boleta_t_f,
                document.getElementById('descripcion_total').value);
        }
        alerta_m('Registro Completado',true);
        setTimeout(() => { window.history.back(); }, 1000);

    } catch (error) {
        console.error('Error durante el desembolso:', error);
    }
});
