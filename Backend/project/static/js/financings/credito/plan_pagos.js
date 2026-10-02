import { PaymentPlan } from '../../class/paymentplan.js'
import { Credit } from '../../class/credit.js'

window.generatePaymentPlan = function () {


    const tbody = document.getElementById('plan-table-body');
    const tfoot = document.getElementById('plan-table-foot');
    const summaryText = document.getElementById('plan-summary-text');
    tbody.innerHTML = '';



    const proposito = document.getElementById('proposito');

    const monto = document.getElementById('monto');
    const plazo = document.getElementById('plazo');
    const tasa_interes = document.getElementById('tasa_interes');
    const forma_de_pago = document.getElementById('forma_de_pago');
    // const frecuencia_pago = document.getElementById('frecuencia_pago');

    const fecha_inicio = document.getElementById('fecha_inicio');
    const tipo_credito = document.getElementById('tipo_credito');
    const customer_id = document.getElementById('customer_id');

    const plazo_gracia = document.getElementById('plazo_gracia');
    const fecha_vencimiento = document.getElementById('fecha_vencimiento');


 

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
        customer_id.value,
        null, plazo_gracia.value
    );

    const plan_pago = new PaymentPlan(credito);
    const plan = plan_pago.recalcular_capital();

    console.log(credito.toJSON());
    //plan-table-body


    plan.forEach(element => {


        const tr = document.createElement('tr');
        tr.className = 'hover:bg-brandBgLight/80 transition-colors border-b border-brandGrayBorder/30';
        tr.innerHTML = `
                    <td class="p-3 text-center font-mono text-brandGrayText font-semibold">${element['mes']}</td>
                    <td class="p-3 font-medium text-darkCard">${transformarFecha(element['fecha_final'])}</td>
                    <td class="p-3 text-right font-mono">Q ${element['monto_prestado']}</td>
                    <td class="p-3 text-right font-mono text-amber-600 font-semibold">Q ${element['intereses']}</td>
                    <td class="p-3 text-right font-mono text-emerald-600 font-semibold">Q ${element['capital']}</td>
                    
                    <td class="p-3 text-right font-mono font-bold text-brandRedDark">Q ${element['cuota']}</td>
                    
                `;
        tbody.appendChild(tr);
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