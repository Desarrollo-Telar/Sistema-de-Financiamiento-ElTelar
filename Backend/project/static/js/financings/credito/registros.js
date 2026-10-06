import {urls_p} from '../../API/urls_api.js'

import {registrar_credito} from '../../API/credito/crear_credito.js'
import {actualizar_credito} from '../../API/credito/actualizar.js'

import { registrar_desembolso } from '../../API/desembolsos/crear_desembolsos.js'

import {registrar_pago} from '../../API/pagos/crear_pago.js'

import {get_credit} from '../../API/credito/obtener_credito.js'


import {guaranteeList} from './garantia.js'
import { showToast } from './style.js';
import {creditos_seleccionados } from './buscadores.js'

let listado_formas = ['APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE', 'REESTRUCTURACIÓN DE CRÉDITO VIGENTE'];

function get_tasaInteres() {
    const tasaInput = document.getElementById('tasa_interes');
    const tasa = tasaInput ? parseFloat(tasaInput.value) || 0 : 0;

    let resultado;
    if (tasa > 1) {
        resultado = (tasa / 12) / 100;
    } else {
        resultado = tasa / 12;
    }

    return resultado.toFixed(3);
}



export async function guardar_credito(monto){
    let formData = new FormData();

    if (document.getElementById('customer_id').value === '') {
        showToast('Debe seleccionar un cliente antes de continuar.', 'error');
        throw new Error('Cliente no seleccionado');
    }

    if (document.getElementById('sucursal_id').value === '') {
        showToast('Debe seleccionar una sucursal antes de continuar.', 'error');
        throw new Error('Sucursal no seleccionada');
    }

    if (document.getElementById('asesor_de_credito').value === '') {
        showToast('Debe seleccionar un asesor de crédito antes de continuar.', 'error');
        throw new Error('Asesor de crédito no seleccionado');
    }
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
    formData.append('is_paid_off',false);
    formData.append('sucursal',document.getElementById('sucursal_id').value);
    formData.append('asesor_de_credito', document.getElementById('asesor_de_credito').value);
    formData.append('plazo_gracia', document.getElementById('plazo_gracia').value);
    formData.append('fecha_finalizacion_gracia', document.getElementById('fecha_finalizacion_gracia').value);
    
    return await registrar_credito(formData);
}

export async function guardar_desembolso(credit_id, forma_desembolso, credito_cancelado=NaN) {
    let formData = new FormData();
    let descripcion = document.getElementById('description')?.value || '';
    
    const montoCredito =
        parseFloat(document.getElementById('monto')?.value) || 0;

    const honorarios =
        parseFloat(document.getElementById('honorarios')?.value) || 0;

    const poliza =
        parseFloat(document.getElementById('poliza_seguro')?.value) || 0;

    const montoDesembolsado =
        parseFloat(document.getElementById('monto_desembolsado')?.value) || 0;

    if (listado_formas.includes(forma_desembolso) && credito_cancelado) {
        try {
            const creditoObtenido = await get_credit(credito_cancelado);
            descripcion = `${descripcion}\nSE ${forma_desembolso}: ${creditoObtenido.codigo_credito}`;
        } catch (e) {
            console.warn("No se pudo obtener la información del crédito anterior:", e);
        }
    }

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

    const totalGastos =
        honorarios + poliza + montoDesembolsado + saldoAnterior;
    
    const montoTotalDesembolsoDiferencia =
        montoCredito -
        (
            saldoAnterior +
            poliza +
            honorarios +
            montoDesembolsado
        );

    formData.append('credit_id', credit_id);
    formData.append('forma_desembolso', forma_desembolso);
    formData.append('monto_credito', montoCredito);
    formData.append('saldo_anterior', saldoAnterior);
    formData.append('honorarios', honorarios);
    formData.append('poliza_seguro', poliza);
    formData.append('monto_desembolsado', montoDesembolsado);
    formData.append('monto_total_desembolso', montoTotalDesembolsoDiferencia);
    formData.append('total_gastos', totalGastos);
    formData.append('description', descripcion);


    return await registrar_desembolso(formData);
    
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
    formData.append('sucursal', document.getElementById('sucursal_id')?.value || '');
    return await registrar_pago(formData);
    
}

export async function registroGarantia(credito_id, suma_total, lista_garantia) {
    try {
        let json = {
            suma_total: suma_total,
            credit_id: credito_id,
            descripcion: document.getElementById('garantia_descripcion_general').value || 'REGISTRO DE GARANTIA',
        };



        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) throw new Error('Token CSRF no encontrado');
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

        let detalles = [];
        if (lista_garantia && lista_garantia.length > 0) {
            detalles = await registrarDetalle(data.id, lista_garantia);
        }
       

        return { garantia: data, detalles };
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}


export async function registrarDetalle(garantia_id, lista_garantia = []) {
    try {
        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        const csrfToken = csrfTokenElement ? csrfTokenElement.getAttribute('content') : '';
        const resultados = [];

        for (let element of lista_garantia) {
            let js = {
                garantia_id: garantia_id,
                tipo_garantia: element.tipo_garantia,
                valor_cobertura: element.valor_cobertura,
                especificaciones: element.especificacion || element.especificaciones
            };

            

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




window.finalizeRegistration = finalizeRegistration

async function registrar_pago_boleta (credito,desembolso,monto, referencia, fecha, boleta, descripcion){

    const respuesta =await guardar_boleta_desembolso(credito, desembolso, monto, referencia, fecha, descripcion, boleta);
    console.log('Respuesta del pago de boleta:', respuesta);
    if (respuesta === undefined) {
        showToast('Error al registrar el pago de boleta.', 'error');
        return null;
    }
    return respuesta;
};

export async function finalizeRegistration(){
    // Validación de campos requeridos
    
    const requiredFields = [
        document.getElementById('proposito'),
        document.getElementById('monto'),
        document.getElementById('plazo'),
        document.getElementById('tasa_interes'),
        document.getElementById('forma_de_pago'),
        document.getElementById('fecha_inicio'),
        document.getElementById('sucursal_id'),
        document.getElementById('asesor_de_credito'),
       
        ];
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('border-red-500');
            isValid = false;
            console.log(`Campo requerido vacío: ${field.id}`);
        } else {
            field.classList.remove('border-red-500');
        }
    });


    
   const forma_desembolso = document.getElementById('forma_desembolso').value;


    console.log(`Listado de Garantias: ${guaranteeList}`);
    console.log(`Creditos a Cancelar: ${creditos_seleccionados}\n `);
    

    if (listado_formas.includes(forma_desembolso) && creditos_seleccionados.length === 0) {
        showToast('Debe seleccionar al menos un crédito vigente para aplicar la ampliación.', 'error');
        isValid = false;
        return;
    }

    if (guaranteeList.length === 0) {
        showToast('Debe registrar al menos una garantía.', 'error');
        isValid = false;
        return;
    }

    if (isValid) {
        
        console.log('Todos los campos requeridos están completos. Procediendo con el registro...');
        const resultado = await registro_formulario(forma_desembolso, guaranteeList, creditos_seleccionados);

        if (resultado && resultado.exito) {
            showToast('Registro completado con éxito.', 'success');
            setTimeout(() => { window.location.href = `/financings/credit/${resultado.credito.id}`; }, 1000);
        }
        return;

    }else{
        showToast('Por favor, complete todos los campos requeridos.', 'error');
        return;

    }




} 



async function registro_formulario(forma_desembolso, listado_garantia, creditos_seleccionados = NaN){
    let credit_id = null;
    try{
        // 1. Lectura del monto principal
        const monto = document.getElementById('monto')?.value || 0;

        const honorarios = parseFloat(document.getElementById('honorarios').value || 0);
        const poliza = parseFloat(document.getElementById('poliza_seguro').value || 0);
        const monto_desembolsado = parseFloat(document.getElementById('monto_desembolsado').value || 0);

        const ref_honorarios = parseFloat(document.getElementById('honorarios_ref').value || 0);
        const ref_poliza = parseFloat(document.getElementById('poliza_ref').value || 0);
        const ref_monto_desembolsado = parseFloat(document.getElementById('monto_desembolsado_ref').value || 0);


        // 2. Guardar Crédito
        const respuestaCredito = await guardar_credito(monto);
        
        credit_id = respuestaCredito.id || respuestaCredito.pk;

        
        if(!respuestaCredito && respuestaCredito.id === undefined){
            showToast('Error al guardar el crédito.', 'error');
            return null;
        }

        // 3. Guardar Desembolso
        const respuestaDesembolso = await guardar_desembolso(credit_id, forma_desembolso, creditos_seleccionados);
  

        if (!respuestaDesembolso && respuestaDesembolso.id === undefined) {
            showToast('Error al guardar el desembolso.', 'error');
            return null;
        }
        
        let respuestaCreditosCancelados = null;
        let respuestaBoleta = null;

        if (creditos_seleccionados.length > 0) {
            for (let creditoId of creditos_seleccionados) {
                respuestaCreditosCancelados = await guardar_desembolso(creditoId, 'CANCELACIÓN DE CRÉDITO VIGENTE');
               

                if (!respuestaCreditosCancelados && respuestaCreditosCancelados.id === undefined) { 

               
                    showToast(`Error al cancelar el crédito con ID: ${creditoId}.`, 'error');
                    return null;
                }

                const formData = new FormData();
                formData.append('is_paid_off', true);
                await actualizar_credito(creditoId, formData);
            }
        }

        if (honorarios > 0 && ref_honorarios != ''){
            respuestaBoleta = await registrar_pago_boleta( 
                credit_id,
                respuestaDesembolso.id,
                honorarios,
                ref_honorarios,
                document.getElementById('honorarios_fecha').value,
                document.getElementById('honorarios_doc').files[0],
                document.getElementById('honorarios_descripcion').value
            );

            
            if (respuestaBoleta === undefined) {
                showToast('Error al registrar el pago de honorarios.', 'error');
                return null;
            }
        }

        if (poliza > 0 && ref_poliza != ''){
            respuestaBoleta = await registrar_pago_boleta(
                credit_id,
                respuestaDesembolso.id,
                poliza,
                ref_poliza,
                document.getElementById('poliza_fecha').value,
                document.getElementById('poliza_doc').files[0],
                document.getElementById('poliza_descripcion').value
            );

            
            if ( respuestaBoleta === undefined) {
                showToast('Error al registrar el pago de póliza de seguro.', 'error');
                return null;
            }
        }

        if (monto_desembolsado > 0 && ref_monto_desembolsado != ''){
            respuestaBoleta =await registrar_pago_boleta(
                credit_id,
                respuestaDesembolso.id,
                monto_desembolsado,
                ref_monto_desembolsado,
                document.getElementById('monto_desembolsado_fecha').value,
                document.getElementById('monto_desembolsado_doc').files[0],
                document.getElementById('monto_desembolsado_descripcion').value
            );

            
            if ( respuestaBoleta === undefined) {
                showToast('Error al registrar el pago del monto desembolsado.', 'error');
                return null;
            }
        }


        // 4. Guardar Garantía y sus detalles (si existen variables globales o pasadas en opciones)
        let respuestaGarantia = null;
        const listaGarantias = listado_garantia || guaranteeList;
        
        const sumaTotalGarantia = document.getElementById('suma_total_garantia').value;

        if (listaGarantias.length > 0) {
            respuestaGarantia = await registroGarantia(credit_id, sumaTotalGarantia, listaGarantias);

           
            if (!respuestaGarantia) {
                showToast('Error al registrar la garantía.', 'error');
                return null;
            }
        }

        return {
            exito: true,
            credito: respuestaCredito,
            desembolso: respuestaDesembolso,
            creditos_cancelados: respuestaCreditosCancelados,
            garantia: respuestaGarantia,
            boleta: respuestaBoleta
        };



    }catch(e){
        console.error('Error en el registro del formulario:', e);
        showToast('Ocurrió un error durante el registro. Por favor, intente nuevamente.', 'error');
        setTimeout(() => { window.location.href = `/financings/credit/delete/${credit_id}`; }, 1000);
    }

}