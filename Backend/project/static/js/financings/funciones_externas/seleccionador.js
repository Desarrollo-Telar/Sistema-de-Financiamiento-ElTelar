
import {ocultar, mostrar} from './ocultar_mostrar.js'
import {actualizarTotalDepositar} from '../credit/desembolso.js'
// COMPONENTES PARA LA SELECCION DE GARANTIA
const tipo_garantia = document.getElementById('tipo_garantia');
const hipoteca = document.getElementById('hipoteca');
const derecho_posesion = document.getElementById('derecho_posesion');
const cheque = document.getElementById('cheque');
const fiador = document.getElementById('fiador');
const mobiliaria = document.getElementById('mobiliaria');
const vehiculo = document.getElementById('vehiculo');

// COMPONENTES PARA LA SELECCION DEL DESEMBOLSO
const forma_desembolso = document.getElementById('forma_desembolso');
const credito_vigente = document.getElementById('credito_vigente');

const honorarios_desembolso = document.getElementById('honorarios_desembolso');
const poliza_seguro_desembolso = document.getElementById('poliza_seguro_desembolso');
const monto_desembolsado_desembolsar = document.getElementById('monto_desembolsado_desembolsar');
const total_a_desembolsar = document.getElementById('total_a_desembolsar');

export function seleccion_desembolso(){
    forma_desembolso.addEventListener('change',function(event){
        const valor_seleccionado = event.target.value;
        if (valor_seleccionado === 'APLICACIÓN GASTOS' ){
            ocultar(credito_vigente);
            mostrar(honorarios_desembolso);
            mostrar(poliza_seguro_desembolso);
            mostrar(monto_desembolsado_desembolsar);
            mostrar(total_a_desembolsar);
            document.getElementById('credito_monto_vigente').value = 0;
            document.getElementById('credito_saldo_capital_vigente').value = 0;
            actualizarTotalDepositar();
            

        } else if (valor_seleccionado === 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE' ){
            ocultar(honorarios_desembolso);
            ocultar(poliza_seguro_desembolso);
            ocultar(monto_desembolsado_desembolsar);
            ocultar(total_a_desembolsar);
            mostrar(credito_vigente);
            actualizarTotalDepositar();

            

        } else if (valor_seleccionado === 'CANCELACIÓN DE CRÉDITO VIGENTE' ){
            ocultar(honorarios_desembolso);
            ocultar(poliza_seguro_desembolso);
            ocultar(monto_desembolsado_desembolsar);
            ocultar(total_a_desembolsar);
            mostrar(credito_vigente);
            actualizarTotalDepositar();

        } else{
            ocultar(credito_vigente);
            ocultar(honorarios_desembolso);
            ocultar(poliza_seguro_desembolso);
            ocultar(monto_desembolsado_desembolsar);
            ocultar(total_a_desembolsar);
            document.getElementById('credito_monto_vigente').value = 0;
            document.getElementById('credito_saldo_capital_vigente').value = 0;

        }
    });

}

export function seleccion_garantia(){
    tipo_garantia.addEventListener('change', function (event) {
        const valor = event.target.value;
        if (valor === 'HIPOTECA') {
            mostrar(hipoteca);
            ocultar(derecho_posesion);
            ocultar(cheque);
            ocultar(fiador);
            ocultar(mobiliaria);
            ocultar(vehiculo);
    
        } else if (valor === 'DERECHO DE POSESIÓN HIPOTECA') {
            ocultar(hipoteca);
            ocultar(cheque);
            mostrar(derecho_posesion);
            ocultar(fiador);
            ocultar(mobiliaria);
            ocultar(vehiculo);
    
    
        } else if (valor === 'FIADOR') {
            ocultar(hipoteca);
            ocultar(derecho_posesion);
            ocultar(cheque);
            mostrar(fiador);
            ocultar(mobiliaria);
            ocultar(vehiculo);
    
        } else if (valor === 'CHEQUE') {
            ocultar(hipoteca);
            ocultar(derecho_posesion);
            mostrar(cheque);
            ocultar(fiador);
            ocultar(mobiliaria);
            ocultar(vehiculo);
    
        } else if (valor === 'VEHICULO') {
            ocultar(hipoteca);
            ocultar(derecho_posesion);
            ocultar(fiador);
            ocultar(mobiliaria);
            mostrar(vehiculo);
    
        } else if (valor === 'MOBILIARIA') {
            ocultar(hipoteca);
            ocultar(derecho_posesion);
            ocultar(fiador);
            mostrar(mobiliaria);
            ocultar(vehiculo);
    
        } else {
            ocultar(hipoteca);
            ocultar(derecho_posesion);
            ocultar(cheque);
            ocultar(fiador);
            ocultar(mobiliaria);
            ocultar(vehiculo);
            console.log('Buenoooo');
        }
    });
    
}