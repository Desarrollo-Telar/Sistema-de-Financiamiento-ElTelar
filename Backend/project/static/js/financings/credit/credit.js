

import {Credit} from '../../class/credit.js'
import {PaymentPlan} from '../../class/paymentplan.js'





const proposito = document.getElementById('proposito'); 
const monto= document.getElementById('monto');
const plazo = document.getElementById('plazo');
const tasa_interes = document.getElementById('tasa_interes');
const forma_de_pago = document.getElementById('forma_de_pago');
//const frecuencia_pago = document.getElementById('frecuencia_pago');

const fecha_inicio = document.getElementById('fecha_inicio');
const tipo_credito = document.getElementById('tipo_credito');
const customer_id = document.getElementById('customer_id');
const tbody_plan = document.getElementById('tbody_plan');

function generar_plan (){
    tbody_plan.innerHTML = '';
    const fechaInicioValue = new Date(fecha_inicio.value);
    
    let credito = new Credit(proposito.value,monto.value,plazo.value,tasa_interes.value,forma_de_pago.value,'MENSUAL',fechaInicioValue,tipo_credito.value,'',customer_id.value);
    let plan_pago = new PaymentPlan(credito);
    let plan = plan_pago.generarPlan();
    console.log(credito.toJSON());
    plan.forEach(element => {
        
        
        var nueva_fila = tbody_plan.insertRow();
        var mes = nueva_fila.insertCell(0);
        mes.textContent = element['mes'];
        var fechaIni = nueva_fila.insertCell(1);
        fechaIni.textContent =  transformarFecha(element['fecha inicio']);
        var fechaVenc = nueva_fila.insertCell(2);
        fechaVenc.textContent = transformarFecha(element['fecha final']);
        var monto = nueva_fila.insertCell(3);
        monto.textContent = 'Q'+element['monto_prestado'];
        var interes = nueva_fila.insertCell(4);
        interes.textContent = 'Q'+element['intereses'];
        var capital = nueva_fila.insertCell(5);
        capital.textContent = 'Q'+element['capital'];
        var cuota = nueva_fila.insertCell(6);
        cuota.textContent = 'Q'+element['cuota'];
        
        
    });
    
}

function transformarFecha(ele){
    // Crear una nueva fecha
    const fecha = new Date(ele);

    // Obtener el día, mes y año
    const dia = fecha.getDate().toString().padStart(2, '0');
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0'); // Los meses en JavaScript empiezan en 0
    const año = fecha.getFullYear();

    // Formatear la fecha como 'dd/mm/yyyy'
    const fechaFormateada = `${dia}/${mes}/${año}`;
    return fechaFormateada
}
document.getElementById('generar_plan').onclick = generar_plan;


/*
proposito.addEventListener('input', function(event){
    credito.proposito = event.target.value;
    plan_pago.credit = credito;

});

monto.addEventListener('input', function(event){
    credito.monto = event.target.value;
    plan_pago.credit = credito;
});

plazo.addEventListener('input',function(event){
    credito.plazo = event.target.value;
    plan_pago.credit = credito;

});

tasa_interes.addEventListener('input',function(event){
    credito.tasaInteres = event.target.value;
    plan_pago.credit = credito;

});

forma_de_pago.addEventListener('input',function(event){
    credito.formaDePago = event.target.value;
    plan_pago.credit = credito;

});

fecha_inicio.addEventListener('input',function(event){
    credito.fechaInicio = event.target.value;

});

tipo_credito.addEventListener('input',function(event){
    credito.tipoCredito = event.target.value;

});
*/

//let credito = new Credit(proposito, monto, plazo, tasa_interes,forma_de_pago , 'MENSUAL', fecha_inicio, tipo_credito, '');
//credito.customerId = customer_id;let plan_pago = new PaymentPlan(credito);



/*
let plan = plan_pago.generarPlan()
plan.forEach(element => {
    console.log(element)
    
});

*/