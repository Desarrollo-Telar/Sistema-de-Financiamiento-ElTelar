
import {guardar_credito,guardar_desembolso,registroGarantia,guardar_boleta_desembolso,registrarDetalle} from './registros_credito.js'

import {ocultar, mostrar} from '../funciones_externas/ocultar_mostrar.js'

import {actualizar_credito} from '../../API/credito/actualizar.js'

import { suma_total, lista_garantia, list_form_data} from './garantia.js'
import { PaymentPlan } from '../../class/paymentplan.js';
import { Credit } from '../../class/credit.js';

const proposito = document.getElementById('proposito');
const monto = document.getElementById('monto');
const plazo = document.getElementById('plazo');
const tasa_interes = document.getElementById('tasa_interes');
const forma_de_pago = document.getElementById('forma_de_pago');
// const frecuencia_pago = document.getElementById('frecuencia_pago');

const fecha_inicio = document.getElementById('fecha_inicio');
const tipo_credito = document.getElementById('tipo_credito');
const customer_id = document.getElementById('customer_id');
const tbody_plan = document.getElementById('tbody_plan');



function generar_plan() {
    tbody_plan.innerHTML = '';

    const fechaInicioValue = new Date(fecha_inicio.value);
    
    const credito = new Credit(
        proposito.value,
        monto.value,
        plazo.value,
        tasa_interes.value,
        forma_de_pago.value,
        'MENSUAL',
        fecha_inicio.value,
        tipo_credito.value,
        null,
        customer_id.value
    );

    const plan_pago = new PaymentPlan(credito);
    const plan = plan_pago.recalcular_capital();

    console.log(credito.toJSON());
    

    plan.forEach(element => {
        const nueva_fila = tbody_plan.insertRow();
        
        nueva_fila.insertCell(0).textContent = element['mes'];
        nueva_fila.insertCell(1).textContent = transformarFecha(element['fecha_inicio']);
        nueva_fila.insertCell(2).textContent = transformarFecha(element['fecha_final']);
        nueva_fila.insertCell(3).textContent = 'Q' + element['monto_prestado'];
        nueva_fila.insertCell(4).textContent = 'Q' + element['intereses'];
        nueva_fila.insertCell(5).textContent = 'Q' + element['capital'];
        nueva_fila.insertCell(6).textContent = 'Q' + element['cuota'];
    });
}

function transformarFecha(ele) {
    const date = new Date(ele);
    const meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ];

    // Extraer día, mes y año
    const day = String(date.getDate()).padStart(2, '0'); // Asegura dos dígitos
    const month = meses[date.getUTCMonth()]; // Meses empiezan desde 0
    const year = date.getFullYear();
    return `${day} de ${month} de ${year}`;
}

document.getElementById('generar_plan').onclick = generar_plan;
let credit, desembolso;
document.getElementById('credito').addEventListener('submit', async function (event) {
    event.preventDefault();
    try {
        if (lista_garantia.length > 0) {
            ocultar(document.getElementById('credito'));
            const forma_desembolso = document.getElementById('forma_desembolso').value;

            let credit_vigente = null;
            if (document.getElementById('credit_vigente')){
                credit_vigente = document.getElementById('credit_vigente').value;
            }
            const saldo_anterior = document.getElementById('credito_saldo_capital_vigente').value;
            const honorarios = parseFloat(document.getElementById('honorarios').value || 0);
            const poliza = parseFloat(document.getElementById('poliza_seguro').value || 0);
            const monto_desembolsado = parseFloat(document.getElementById('monto_desembolsado').value || 0);

            const registrar_pago_boleta = async (monto, referencia, fecha, boleta, descripcion) => {
                console.log('esperar...');
                await guardar_boleta_desembolso(credit.id, desembolso.id, monto, referencia, fecha, descripcion, boleta);
            };

            

            switch (forma_desembolso) {
                case 'APLICACIÓN GASTOS':
                    const monto_g = parseFloat(document.getElementById('monto').value).toFixed(2);
                    credit = await guardar_credito(monto_g);
                    desembolso = await guardar_desembolso(credit.id, 'APLICACIÓN GASTOS');

                    if (honorarios > 0) {
                        const boleta_h = document.getElementById('boleta_honorarios').files[0];
                        await registrar_pago_boleta(honorarios,
                            document.getElementById('numero_referencia_honorarios').value,
                            document.getElementById('fecha_emision_honorarios').value,
                            boleta_h,
                            document.getElementById('descripcion_honorarios').value);
                    }
                    if (poliza > 0) {
                        const boleta_p = document.getElementById('boleta_poliza').files[0];
                        await registrar_pago_boleta(poliza,
                            document.getElementById('numero_referencia_poliza').value,
                            document.getElementById('fecha_emision_poliza').value,
                            boleta_p,
                            document.getElementById('descripcion_poliza').value);
                    }
                    if (monto_desembolsado > 0) {
                        const boleta_monto_d = document.getElementById('boleta_monto_desembolsado').files[0];
                        await registrar_pago_boleta(monto_desembolsado,
                            document.getElementById('numero_referencia_monto_desembolsado').value,
                            document.getElementById('fecha_emision_monto_desembolsado').value,
                            boleta_monto_d,
                            document.getElementById('descripcion_monto_desembolsado').value);
                    }

                    const garantia = await registroGarantia(credit.id);
                    console.log(garantia);
                    
                    Swal.fire({
                        icon: "success",
                        title: `Registro Completado`,
                        text: '¡Formulario enviado con éxito!',
                        timer: 10000,
                        showConfirmButton: false,
                    });
                    setTimeout(() => { window.location.href = `/financings/credit/${credit.id}`; }, 10000);
                    mostrar(document.getElementById('credito'));
                    break;

                case 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE':
                    const monto_credito = document.getElementById('monto').value;
                    const nuevo_monto = parseFloat(monto_credito);
                    const m_a = parseFloat(nuevo_monto).toFixed(2);

                    const formData = new FormData();
                    formData.append('is_paid_off', true);
                    

                    credit = await guardar_credito(m_a);
                    desembolso = await guardar_desembolso(credit.id, document.getElementById('forma_desembolso').value, credit_vigente);
                    await guardar_desembolso(credit_vigente, 'CANCELACIÓN DE CRÉDITO VIGENTE');
                    await actualizar_credito(credit_vigente, formData);

                    if (honorarios > 0) {
                        const boleta_h = document.getElementById('boleta_honorarios').files[0];
                        await registrar_pago_boleta(honorarios,
                            document.getElementById('numero_referencia_honorarios').value,
                            document.getElementById('fecha_emision_honorarios').value,
                            boleta_h,
                            document.getElementById('descripcion_honorarios').value);
                    }
                    if (poliza > 0) {
                        const boleta_p = document.getElementById('boleta_poliza').files[0];
                        await registrar_pago_boleta(poliza,
                            document.getElementById('numero_referencia_poliza').value,
                            document.getElementById('fecha_emision_poliza').value,
                            boleta_p,
                            document.getElementById('descripcion_poliza').value);
                    }
                    if (monto_desembolsado > 0) {
                        const boleta_monto_d = document.getElementById('boleta_monto_desembolsado').files[0];
                        await registrar_pago_boleta(monto_desembolsado,
                            document.getElementById('numero_referencia_monto_desembolsado').value,
                            document.getElementById('fecha_emision_monto_desembolsado').value,
                            boleta_monto_d,
                            document.getElementById('descripcion_monto_desembolsado').value);
                    }

                    const garantiaAmpliacion = await registroGarantia(credit.id);                    
                    console.log(garantiaAmpliacion);
                    Swal.fire({
                        icon: "success",
                        title: `Registro Completado`,
                        text: '¡Formulario enviado con éxito!',
                        timer: 10000,
                        showConfirmButton: false,
                    });
                    setTimeout(() => { window.location.href = `/financings/credit/${credit.id}`; }, 10000);
                    mostrar(document.getElementById('credito'));
                    break;

                case 'CANCELACIÓN DE CRÉDITO VIGENTE':
                    const monto_c = parseFloat(saldo_anterior).toFixed(2);

                    const formDataCancel = new FormData();
                    formDataCancel.append('is_paid_off', true);
                    await actualizar_credito(credit_vigente, formDataCancel);

                    credit = await guardar_credito(monto_c);
                    desembolso = await guardar_desembolso(credit.id);

                    if (honorarios > 0) {
                        const boleta_h = document.getElementById('boleta_honorarios').files[0];
                        await registrar_pago_boleta(honorarios,
                            document.getElementById('numero_referencia_honorarios').value,
                            document.getElementById('fecha_emision_honorarios').value,
                            boleta_h,
                            document.getElementById('descripcion_honorarios').value);
                    }
                    if (poliza > 0) {
                        const boleta_p = document.getElementById('boleta_poliza').files[0];
                        await registrar_pago_boleta(poliza,
                            document.getElementById('numero_referencia_poliza').value,
                            document.getElementById('fecha_emision_poliza').value,
                            boleta_p,
                            document.getElementById('descripcion_poliza').value);
                    }
                    if (monto_desembolsado > 0) {
                        const boleta_monto_d = document.getElementById('boleta_monto_desembolsado').files[0];
                        await registrar_pago_boleta(monto_desembolsado,
                            document.getElementById('numero_referencia_monto_desembolsado').value,
                            document.getElementById('fecha_emision_monto_desembolsado').value,
                            boleta_monto_d,
                            document.getElementById('descripcion_monto_desembolsado').value);
                    }

                    const garantiaCancel = await registroGarantia(credit.id);
                    
                    console.log(garantiaCancel);
                    Swal.fire({
                        icon: "success",
                        title: `Registro Completado`,
                        text: '¡Formulario enviado con éxito!',
                        timer: 10000,
                        showConfirmButton: false,
                    });
                    setTimeout(() => { window.location.href = `/financings/credit/${credit.id}`; }, 10000);
                    mostrar(document.getElementById('credito'));
                    break;
                    

                default:
                    Swal.fire({
                        icon: "error",
                        title: 'Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.',
                        text: 'No se puede enviar, debido a que no ha seleccionado ningún tipo de desembolso',
                        timer: 10000,
                        showConfirmButton: false,
                    });
                    mostrar(document.getElementById('credito'));
                    break;
            }
        }
    } catch (error) {
        console.error('Error al registrar los datos:', error);

        if (error.response) {
            console.error('Error en la respuesta del servidor:', error.response.data);
            Swal.fire({
                icon: "error",
                title: `Error ${error.response.status}`,
                text: error.response.data.message || 'Ocurrió un problema en el servidor.',
                timer: 10000,
                showConfirmButton: false,
            });
        } else if (error.request) {
            console.error('Error en la solicitud:', error.request);
            Swal.fire({
                icon: "error",
                title: `Sin respuesta del servidor`,
                text: `No se obtuvo respuesta del servidor. Por favor, inténtalo más tarde.`,
                timer: 10000,
                showConfirmButton: false,
            });
        } else {
            console.error('Error:', error.message);
            Swal.fire({
                icon: "error",
                title: `Error inesperado`,
                text: error.message,
                timer: 10000,
                showConfirmButton: false,
            });
        }
        setTimeout(() => { window.location.href = `/financings/credit/delete/${credit.id}`; }, 10000);
        mostrar(document.getElementById('credito'));
    }
});
