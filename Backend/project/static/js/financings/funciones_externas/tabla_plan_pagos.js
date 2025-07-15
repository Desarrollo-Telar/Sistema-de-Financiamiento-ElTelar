import { PaymentPlan } from '../../class/paymentplan.js'
import { Credit } from '../../class/credit.js'

export function generar_plan() {
    const tbody_plan = document.getElementById('tbody_plan');
    const proposito = document.getElementById('proposito');
    const monto = document.getElementById('monto');
    const plazo = document.getElementById('plazo');
    const tasa_interes = document.getElementById('tasa_interes');
    const forma_de_pago = document.getElementById('forma_de_pago');
    // const frecuencia_pago = document.getElementById('frecuencia_pago');

    const fecha_inicio = document.getElementById('fecha_inicio');
    const tipo_credito = document.getElementById('tipo_credito');
    const customer_id = document.getElementById('customer_id');

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