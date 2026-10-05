import { PaymentPlan } from '../../class/paymentplan.js'
import { Credit } from '../../class/credit.js'

export function generar_plan() {
    const tbody_plan = document.getElementById('tbody_plan');
    const proposito = '';
    const monto = document.getElementById('total_value_of_the_product_or_service');
    const plazo = document.getElementById('plazo');
    const tasa_interes = document.getElementById('tasa_interes');
    const forma_de_pago = document.getElementById('forma_de_pago');
    // const frecuencia_pago = document.getElementById('frecuencia_pago');

    const fecha_inicio = document.getElementById('fecha_inicio');
    const tipo_credito = document.getElementById('type_of_product_or_service');
    const plazo_gracia = document.getElementById('plazo_garantia');
    const customer_id = '';

    const tfoot = document.getElementById('plan-table-foot');

    tbody_plan.innerHTML = '';

    const fechaInicioValue = new Date(fecha_inicio.value);

    const credito = new Credit(
        proposito,
        monto.value,
        plazo.value,
        tasa_interes.value,
        forma_de_pago.value,
        'MENSUAL',
        fecha_inicio.value,
        tipo_credito.value,
        null,
        customer_id,null,plazo_gracia.value
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
    tfoot.innerHTML = `
                <tr>
                    <td colspan="3" class="p-3 uppercase">Totales del Plan</td>
                    <td class="p-3 text-right font-mono text-emerald-700">Q ${plan_pago.calculo_total_interes().toFixed(2)}</td>
                    <td class="p-3 text-right font-mono text-amber-700">Q ${plan_pago.calculo_total_capital().toFixed(2)}</td>
                    <td class="p-3 text-right font-mono font-bold text-brandRedDark">Q ${plan_pago.calculo_total_cuotas().toFixed(2)}</td>
                   
                </tr>
            `;
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