import { Credit } from '../../class/credit.js';
import { PaymentPlan } from '../../class/paymentplan.js';
import { suma_total, lista_garantia } from './garantia.js'
import {desembolso} from './disbursement.js'

import {urls, urls_p} from '../../API/urls_api.js'
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
/*
function generar_plan() {
    tbody_plan.innerHTML = '';

    const fechaInicioValue = new Date(fecha_inicio.value);


    let credito = new Credit(proposito.value, monto.value, plazo.value, tasa_interes.value, forma_de_pago.value, 'MENSUAL', fechaInicioValue, tipo_credito.value, null, customer_id.value);

    let plan_pago = new PaymentPlan(credito);
    let plan = plan_pago.generarPlan();
    console.log(credito.toJSON());
    plan.forEach(element => {
        var nueva_fila = tbody_plan.insertRow();
        var mes = nueva_fila.insertCell(0);
        mes.textContent = element['mes'];
        var fechaIni = nueva_fila.insertCell(1);
        fechaIni.textContent = transformarFecha(element['fecha inicio']);
        var fechaVenc = nueva_fila.insertCell(2);
        fechaVenc.textContent = transformarFecha(element['fecha final']);
        var monto = nueva_fila.insertCell(3);
        monto.textContent = 'Q' + element['monto_prestado'];
        var interes = nueva_fila.insertCell(4);
        interes.textContent = 'Q' + element['intereses'];
        var capital = nueva_fila.insertCell(5);
        capital.textContent = 'Q' + element['capital'];
        var cuota = nueva_fila.insertCell(6);
        cuota.textContent = 'Q' + element['cuota'];
    });
}
*/
/*
function generar_plan() {
    tbody_plan.innerHTML = '';

    const fechaInicioValue = new Date(fecha_inicio.value);

    let credito = new Credit(proposito.value, monto.value, plazo.value, tasa_interes.value, forma_de_pago.value, 'MENSUAL', fechaInicioValue, tipo_credito.value, null, customer_id.value);
    let plan_pago = new PaymentPlan(credito);
    let plan = plan_pago.generarPlan();

    console.log(credito.toJSON());

    plan.forEach(element => {
        var nueva_fila = tbody_plan.insertRow();
        var mes = nueva_fila.insertCell(0);
        mes.textContent = element['mes'];
        var fechaIni = nueva_fila.insertCell(1);
        fechaIni.textContent = transformarFecha(element['fecha inicio']);
        var fechaVenc = nueva_fila.insertCell(2);
        fechaVenc.textContent = transformarFecha(element['fecha final']);
        var monto = nueva_fila.insertCell(3);
        monto.textContent = 'Q' + element['monto_prestado'];
        var interes = nueva_fila.insertCell(4);
        interes.textContent = 'Q' + element['intereses'];
        var capital = nueva_fila.insertCell(5);
        capital.textContent = 'Q' + element['capital'];
        var cuota = nueva_fila.insertCell(6);
        cuota.textContent = 'Q' + element['cuota'];
    });
}
*/
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
    const fecha = new Date(ele);
    const dia = fecha.getDate().toString().padStart(2, '0');
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0');
    const año = fecha.getFullYear();
    return `${dia}/${mes}/${año}`;
}

document.getElementById('generar_plan').onclick = generar_plan;
/*
document.getElementById('credito').addEventListener('submit', async function (event) {
    event.preventDefault();



    
    try {
        let credito = new Credit();
        credito.proposito = proposito.value;
        credito.monto = monto.value;
        credito.plazo = plazo.value;
        credito.tasaInteres = tasa_interes.value; // Asegúrate de que este valor es el correcto
        credito.formaDePago = forma_de_pago.value;
        credito.frecuenciaPago = 'MENSUAL';
        credito.fechaInicio = new Date(fecha_inicio.value);
        credito.tipoCredito = tipo_credito.value;
        credito.customerId = customer_id.value;
        credito.fechaVencimiento = new Date(fecha_inicio.value); // Corregido para obtener la fecha de vencimiento correcta
        credito.fechaVencimiento.setFullYear(credito.fechaVencimiento.getFullYear() + 1);
        
        console.log(credito.toJSON());

        const credi = await registrarCredito('http://127.0.0.1:8000/financings/api/credit/', credito);
        console.log('Credito Registrado', credi);
        const garantia = await registroGarantia('http://127.0.0.1:8000/financings/api/garantia/',credi.id)
        console.log(garantia)
        alert('¡Formulario enviado con éxito!');
        window.location.href = '/customers/';
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }
    
});
*/
document.getElementById('credito').addEventListener('submit', async function (event) {
    event.preventDefault();

    try {

        if (lista_garantia.length > 0) {
            let credito = new Credit();
            credito.proposito = proposito.value;
            credito.monto = monto.value;
            credito.plazo = plazo.value;
            credito.tasaInteres = tasa_interes.value;
            credito.formaDePago = forma_de_pago.value;
            credito.frecuenciaPago = 'MENSUAL';
            credito.fechaInicio = new Date(fecha_inicio.value);
            credito.tipoCredito = tipo_credito.value;
            credito.customerId = customer_id.value;
            credito.fechaVencimiento = new Date(fecha_inicio.value);
            credito.fechaVencimiento.setFullYear(credito.fechaVencimiento.getFullYear() + 1);

            console.log(credito.toJSON());
            const credi = await registrarCredito(urls_p.api_url_credit, credito);
            console.log('Credito Registrado', credi);
            const garantia = await registroGarantia(urls_p.api_url_garantia, credi.id);
            console.log(garantia);
            const desembolsos = await registrarDesembolso(urls_p.api_url_desembolso,credi.id);
            console.log(desembolsos)

            alert('¡Formulario enviado con éxito!');
            window.location.href = `/financings/credit/${credi.id}`;

        }else{
            alert('NO SE HA REGISTRADO NINGUNA GARANTIA')
        }


    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }
});

async function registrarCredito(url, credito) {
    try {
        let json = {
            customer_id: parseInt(document.getElementById('customer_id').value),
            destino_id: null,
            fecha_inicio: document.getElementById('fecha_inicio').value,
            fecha_vencimiento: document.getElementById('fecha_vencimiento').value,
            forma_de_pago: credito.formaDePago,
            frecuencia_pago: 'MENSUAL',
            monto: credito.monto,
            plazo: credito.plazo,
            proposito: credito.proposito,
            tasa_interes: credito.tasaInteres,
            tipo_credito: credito.tipoCredito,
        };
        console.log(json);

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response = await axios.post(url, json, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        alert('ERROR: ',error);
        console.error('Error:', error);
        throw error;
    }
}



/*
async function registroGarantia(url, credito_id) {

    try {
        let json = {
            suma_total: suma_total,
            credit_id: credito_id
        };
        console.log(json);

        // Obtener el token CSRF del meta tag
        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) {
            throw new Error('CSRF token not found');
        }
        const csrfToken = csrfTokenElement.getAttribute('content');

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
            },
            body: JSON.stringify(json)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        const detalle = await registrarDetalle('http://127.0.0.1:8000/financings/api/detalle_garantia/',data.id);
        console.log(detalle);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }

}
*/
async function registroGarantia(url, credito_id) {
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

        const response = await fetch(url, {
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
        const detalle = await registrarDetalle(urls_p.api_url_detalle_garantia, data.id);
        console.log(detalle);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}


async function registrarDetalle(url, garantia_id) {
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        for (let element of lista_garantia) {
            let js = {
                garantia_id: garantia_id,
                tipo_garantia: element['tipo_garantia'],
                valor_cobertura: element['valor_cobertura'],
                especificaciones: element['especificacion'],
            };
            console.log(`DETALLE DE GARANTIA ${JSON.stringify(js)}`)

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en las cabeceras
                },
                body: JSON.stringify(js)
            });

            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.status}`);
            }

            const data = await response.json();
            console.log('Respuesta de la API:', data);
        }

    } catch (error) {
        console.error('Error en el envío de detalles:', error);
        throw error;
    }
}

async function registrarDesembolso(url, credit_id){
    try {
        desembolso.credit_id = credit_id

        

        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) {
            throw new Error('CSRF token not found');
        }
        const csrfToken = csrfTokenElement.getAttribute('content');

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(desembolso.toJson())
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }

}