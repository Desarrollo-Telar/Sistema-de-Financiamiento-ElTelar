import {oculto} from './ocultar_todo.js'
import {tipo_codigo} from './tipo_codigo_egreso.js'

// Atributos para egresos(gastos)


const input_id_codigo_egreso = document.getElementById('id_codigo_egreso');
const label_id_codigo_egreso = document.querySelector('label[for="id_codigo_egreso"]')|| NaN;

if (input_id_codigo_egreso){
    input_id_codigo_egreso.addEventListener("input", (event) => {
        tipo_codigo(event.target.value,true);
    });
    
    tipo_codigo(input_id_codigo_egreso.value, false);
}







