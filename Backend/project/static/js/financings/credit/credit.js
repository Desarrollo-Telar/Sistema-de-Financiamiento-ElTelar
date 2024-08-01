import { Credit } from '../../class/credit.js';
import { PaymentPlan } from '../../class/paymentplan.js';

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

function transformarFecha(ele) {
    const fecha = new Date(ele);
    const dia = fecha.getDate().toString().padStart(2, '0');
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0');
    const año = fecha.getFullYear();
    return `${dia}/${mes}/${año}`;
}

document.getElementById('generar_plan').onclick = generar_plan;

document.getElementById('credito').addEventListener('submit', async function(event) {
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
        alert('¡Formulario enviado con éxito!');
        window.location.href = '/customers/';
    } catch (error) {
        console.error('Error al registrar los datos:', error);
        alert('Hubo un error al enviar el formulario. Por favor, inténtalo de nuevo.');
    }
});

async function registrarCredito(url, credito) {
    try {
        let json = {
            customer_id: credito.customerId,
            destino_id: credito.destinoId,
            fecha_inicio: credito.fechaInicio.toISOString().split('T')[0],
            fecha_vencimiento: credito.fechaVencimiento.toISOString().split('T')[0],
            forma_de_pago: credito.formaDePago,
            frecuencia_pago: credito.frecuenciaPago,
            monto: credito.monto,
            plazo: credito.plazo,
            proposito: credito.proposito,
            tasa_interes: credito.tasaInteres, // Asegúrate de que este valor es el correcto
            tipo_credito: credito.tipoCredito
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
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
